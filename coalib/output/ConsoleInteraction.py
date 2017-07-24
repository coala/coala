@botcmd
def cobot_show_my_errors(self, msg, args):
    # Will respond to `!cobot show my errors`
    errors = db.Query.find(Errors.assignee == msg.frm).all()
    yield "@{} is assigned to {} issues,".format(msg.frm, len(errors))
    for error in errors:
        yield error.message + '\n'