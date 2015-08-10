import queue
from queue import Empty
import traceback
from collections import Iterable

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.LocalBear import LocalBear
from coalib.misc.Constants import Constants
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.processes.communication.LogMessage import LogMessage, LOG_LEVEL
from coalib.misc.i18n import _
from coalib.results.Result import Result


def send_msg(message_queue, timeout, log_level, *args, delimiter=' ', end=''):
    """
    Puts message into message queue for a LogPrinter to present to the user.

    :param message_queue: The queue to put the message into and which the
                          LogPrinter reads.
    :param timeout:       The queue blocks at most timeout seconds for a free
                          slot to execute the put operation on. After the
                          timeout it returns queue Full exception.
    :param log_level:     The log_level i.e Error,Debug or Warning.It is sent
                          to the LogPrinter depending on the message.
    :param args:          This includes the elements of the message.
    :param delimiter:     It is the value placed between each arg. By default
                          it is a ' '.
    :param end:           It is the value placed at the end of the message.
    """
    output = str(delimiter).join(str(arg) for arg in args) + str(end)
    message_queue.put(LogMessage(log_level, output),
                      timeout=timeout)


def validate_results(message_queue, timeout, result_list, name, args, kwargs):
    """
    Validates if the result_list passed to it contains valid set of results.
    That is the result_list must itself be a list and contain objects of the
    instance of Result object. If any irregularity is found a message is put in
    the message_queue to present the irregularity to the user. Each result_list
    belongs to an execution of a bear.

    :param message_queue: A queue that contains messages of type
                          errors/warnings/debug statements to be printed in the
                          Log.
    :param timeout:       The queue blocks at most timeout seconds for a free
                          slot to execute the put operation on. After the
                          timeout it returns queue Full exception.
    :param result_list:   The list of results to validate.
    :param name:          The name of the bear executed.
    :param args:          The args with which the bear was executed.
    :param kwargs:        The kwargs with which the bear was executed.
    :return:              Returns None if the result_list is invalid. Else it
                          returns the result_list itself.
    """
    if result_list is None:
        return None

    if not isinstance(result_list, Iterable):
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.ERROR,
                 _("The results from the bear {bear} couldn't be processed "
                   "with arguments {arglist}, {kwarglist}.")
                 .format(bear=name, arglist=args, kwarglist=kwargs))
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.DEBUG,
                 _("The return value of the {bear} is an instance of {ret}"
                   " but should be an instance of list.")
                 .format(bear=name, ret=result_list.__class__))
        return None

    # If it's already a list it won't change it
    result_list = list(result_list)

    for result in result_list:
        if not isinstance(result, Result):
            send_msg(message_queue,
                     timeout,
                     LOG_LEVEL.ERROR,
                     _("The results from the bear {bear} could only be "
                       "partially processed with arguments {arglist}, "
                       "{kwarglist}")
                     .format(bear=name, arglist=args, kwarglist=kwargs))
            send_msg(message_queue,
                     timeout,
                     LOG_LEVEL.DEBUG,
                     _("One of the results in the list for the bear {bear} is "
                       "an instance of {ret} but it should be an instance of "
                       "Result")
                     .format(bear=name, ret=result.__class__))
            result_list.remove(result)

    return result_list


def run_bear(message_queue, timeout, bear_instance, *args, **kwargs):
    """
    This method is responsible for executing the instance of a bear. It also
    reports or logs errors if any occur during the execution of that bear
    instance.

    :param message_queue: A queue that contains messages of type
                          errors/warnings/debug statements to be printed in the
                          Log.
    :param timeout:       The queue blocks at most timeout seconds for a free
                          slot to execute the put operation on. After the
                          timeout it returns queue Full exception.
    :param bear_instance: The instance of the bear to be executed.
    :param args:          The arguments that are to be passed to the bear.
    :param kwargs:        The keyword arguments that are to be passed to the
                          bear.
    :return:              Returns a valid list of objects of the type Result
                          if the bear executed succesfully. None otherwise.
    """
    if kwargs.get("dependency_results", True) is None:
        del kwargs["dependency_results"]

    name = bear_instance.__class__.__name__

    try:
        result_list = bear_instance.execute(*args,
                                            **kwargs)
    except:
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.ERROR,
                 _("The bear {bear} failed to run with the arguments "
                   "{arglist}, {kwarglist}. Skipping bear...")
                 .format(bear=name, arglist=args, kwarglist=kwargs))
        send_msg(message_queue,
                 timeout,
                 LOG_LEVEL.DEBUG,
                 _("Traceback for error in bear {bear}:")
                 .format(bear=name),
                 traceback.format_exc(),
                 delimiter="\n")

        return None

    return validate_results(message_queue,
                            timeout,
                            result_list,
                            name,
                            args,
                            kwargs)


class Job:
    def __init__(self, function, args, kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def apply(self, message_queue, timeout):
        try:
            self.function(*self.args,
                          message_queue=message_queue,
                          **self.kwargs)
        except Exception as exp:
            send_msg(message_queue,
                     timeout,
                     LOG_LEVEL.ERROR,
                     _("The bear {bear} failed to run with the arguments "
                       "{arglist}, {kwarglist}. Skipping bear...")
                     .format(bear=name, arglist=args, kwarglist=kwargs))
            send_msg(message_queue,
                     timeout,
                     LOG_LEVEL.DEBUG,
                     _("Traceback for error in bear {bear}:")
                     .format(bear=name),
                     traceback.format_exc(),
                     delimiter="\n")



def process_jobs(job_queue,
                 message_queue,
                 result_dict,
                 timeout=0):
    try:
        while True:
            job = job_queue.get(timeout=timeout)
            result_dict[job] = job.apply(message_queue, timeout)
    except Empty:
        pass
