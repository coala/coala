Pdb Basics
==========

pdb - The Python Debugger
-------------------------

The module ``Pdb`` defines an interactive source code debugger for Python programs. It supports setting (conditional) breakpoints and single stepping at the source line level, inspection of stack frames, source code listing, and evaluation of arbitrary Python code in the context of any stack frame. It also supports post-mortem debugging and can be called under program control.

``This is a basic guide of Pdb/Python_Debugger for Begineers``

How to install Pdb
------------------

``Pdb`` is included with both ``Pyhton 2`` and ``Pyhton 3``,just import it.

Run Pdb
-------

        **Run from Within Your Program**:

	.. note::

			The typical usage to break into the debugger from a running program is to insert.:
					
					- **import pdb**
					
					- **pdb.set_trace()** 
					
			Import inside the pyhton file you want to debug.

			The debugger’s prompt is **(Pdb)**.
	

	About *set_trace()*:
		Enter the debugger at the calling stack frame. This is useful to hard-code a breakpoint at a given point in a program, even if the code is not otherwise being debugged (e.g. when an assertion fails).

	**Here is an example**:

		Lets say we created a Python file ``Filename.py``:

		.. code:: python

				import pdb 
				def example(x, y):
					y *= 2
					x *= 3
					z = x+y
					return z


				x = 15
				y = 10
				z = 3
				pdb.set_trace()
				example(5,10)
				print('z = '+ str(z))
				d = example(2,3)
				print('d = '+ str(d))

	**Run it on terminal**:

			**$ python3 Filename.py**.
			
			Replace ``python3`` with ``python`` if you are using Python2.
			Here we are using ``Python 3``


.. note::
		
		Below example are tested on ``Python 3``




Few **Debugger Commands**:
--------------------------
	
	**Here is the list of few** ``Pdb``  **Debugger Command**:


	- **l**
		Executes the current line and moves to the next in the current file.
		List source code for the current file. Without arguments, list 11 lines around the current line or continue the previous listing. With . as argument, list 11 lines around the current line. With one argument, list 11 lines around at that line. With two arguments, list the given range; if the second argument is less than the first, it is interpreted as a count.

		The current line in the current frame is indicated by ``->``. If an exception is being debugged, the line where the exception was originally raised or propagated is indicated by ``>>``, if it differs from the current line.

		New in version 3.2: The ``>>`` marker.


		**Here is an example**:

				
				Run:
				$ python3 Filename.py

				.. code:: python

					> /home/user_name/Filename.py(15)<module>()
					-> example(5,10)
					(Pdb) l
					 10  	
					 11  	x = 15
					 12  	y = 10
					 13  	z = 3
					 14  	pdb.set_trace()
					 15  ->	z = example(5,10)
					 16  	print('z = '+ str(z))
					 17  	d = example(2,3)
					 18  	print('d = '+ str(d))
					[EOF]
					(Pdb)q


	- **s**
		Execute the current line, stop at the first possible occasion (either in a function that is called or on the next line in the current function).

		**Here is an example**:

				
				Run:
				$ python3 Filename.py
				
				**OUTPUT**

				.. code:: python

					> /home/user_name/Filename.py(15)<module>()
					-> example(5,10)
					(Pdb) s
					--Call--
					> /home/user_name/Filename.py(3)example()
					-> def example(x, y):
					(Pdb)q




	- **n**
		Continue execution until the next line in the current function is reached or it returns.
		(next executes called functions, only stopping at the next line in the current program.)

		**Here is an example**:

				Run:
				$ python3 Filename.py,
				
				**OUTPUT**


				.. code:: python

					> /home/user_name/Filename.py(15)<module>()
					-> example(5,10)
					(Pdb) l
					> /home/user_name/Filename.py(16)<module>()
					-> print('z = '+ str())
					(Pdb)q

	- **p**	
		Evaluate the expression in the current context and print its value.

		**Here is an example**:

				Run:
				$ python3 Filename.py,
				
				**OUTPUT**


				.. code:: python

					> /home/user_name/Filename.py(15)<module>()
					-> z = example(5,10)
					(Pdb) n
					> /home/user_name/Filename.py(16)<module>()
					-> print('z = '+ str(z))
					(Pdb) p(z)
					35
					(Pdb)q

	- **q**
		Quit from the debugger. The program being executed is aborted.

		**Here is an example**:

				Run:
				$ python3 Filename.py,
				
				**OUTPUT**

				.. code:: python

					> /home/user_name/Filename.py(15)<module>()
					-> z = example(5,10)
					(Pdb) n
					> /home/user_name/Filename.py(16)<module>()
					-> print('z = '+ str(z))
					(Pdb) p(z)
					35
					(Pdb)q


	- **b [int]**
		Set break point at line number (eg. ``b 16``)

		**Here is an example**:

				Run:
				$ python3 Filename.py,
				
				**OUTPUT**

				.. code:: python

					> /home/user_name/Filename.py(15)<module>()
					-> z = example(5,10)
					(Pdb) b 16
					Breakpoint 1 at /home/user_name/Filename.py:16
					(Pdb)q

	- **b**
		Show list of all break point


		**Here is an example**:

				Run:
				$ python3 Filename.py,
				
				**OUTPUT**

				.. code:: python

					> /home/user_name/Filename.py(15)<module>()
					-> z = example(5,10)
					(Pdb) b 16
					Breakpoint 1 at /home/user_name/Filename.py:16
					(Pdb) b
					Num Type         Disp Enb   Where
					1   breakpoint   keep yes   at /home/user_name/Filename.py:16
					(Pdb)q

	- **b [func]**
		Break at Function name

		**Here is an example**:

				Run:
				$ python3 Filename.py,
				
				**OUTPUT**

				.. code:: python


					> /home/User_name/Filename.py(15)<module>()
					-> z = example(5,10)
					(Pdb) b example
					Breakpoint 1 at /home/user_name/Filename.py:3
					(Pdb)q
		




	- **cl**	
		Clear all break point

		**Here is an example**:

				Run:
				$ python3 Filename.py,
				
				**OUTPUT**


				.. code:: python


					> /home/user_name/Filename.py(15)<module>()
					-> z = example(5,10)
					(Pdb) b 16
					Breakpoint 1 at /home/user_name/Filename.py:16
					(Pdb) b
					Num Type         Disp Enb   Where
					1   breakpoint   keep yes   at /home/user_name/Filename.py:16
					(Pdb) cl
					Clear all breaks? y
					Deleted breakpoint 1 at /home/user_name/Filename.py:16
					(Pdb)q

	- **cl [int]**
	
		Clear the the specific break point on a line (eg. ``cl 1``)	

		**Here is an example**:

				Run:
				$ python3 Filename.py,
				
				**OUTPUT**


				.. code:: python


					> /home/user_name/Filename.py(15)<module>()
					-> z = example(5,10)
					(Pdb) b 3
					Breakpoint 1 at /home/vaibhav/pbd.py:3
					(Pdb) cl 1
					Deleted breakpoint 1 at /home/vaibhav/pbd.py:3
					(Pdb)q



.. note::


	**For more detail and commands of Pdb go through**:

		`Pdb Detailed Explanation for python 2
		<https://docs.python.org/2/library/pdb.html>`_.

		`Pdb Detailed Explanation for python 3
		<https://docs.python.org/3/library/pdb.html>`_.
























				

































	
































