Python ``raise`` as a Function
==============================

Raise exceptions with a function instead of a statement.

Provides a minimal, clean and portable interface for raising
exceptions with all the advantages of functions over syntax.


Why
---

I want to be able to work with exceptions in a way that is:

1. *Intuitive* to use and see in code.
2. *Generic* and *flexible*, empowering *reuse*.
3. *Portable* to all versions of Python I might want to use.

Python is a great language, and modern Python in particular takes a
nice approach to exceptions.

In my code, I've often found myself writing interfaces that combine
the intuitive nature of Python 3's ``raise`` and ``with_traceback``,
the generic and flexible pattern of raising exceptions in other
coroutines or threads of execution as exemplified by the ``throw``
method on Python generators, and the inherently portable and powerfully
reusable and composable form of a basic function.

The interface provided by this module, the function signature taking
an ``exception`` (either an instance *or* a type) and an optional
``traceback`` instance, is what I found myself arriving at that met all
of these criteria. It has served me well in code that I've worked on,
and I'm submitting it to the world in the hope that others will either
find it useful and build upon it or point out flaws in my approach.

If you have a more specific "why" question, I recorded my reasons for a
lot of the specific choices here in the `Design Decisions`_ section.


Versioning
----------

This library's version numbers follow the `SemVer 2.0.0 specification
<https://semver.org/spec/v2.0.0.html>`_.

The current version number is available in the variable ``__version__``
as is normal for Python modules.


Installation
------------

::

    pip install raise

**If** you need or want to get it *manually*, or you need the "no
traceback" variant, see the `Advanced/Manual Installation`_ section
for suggestions/tips.


Usage
-----

Import the ``raise_`` function from the ``raise_`` module:

.. code:: python

    from raise_ import raise_

Then you can raise things in a fairly intuitive manner:

1. Raising an exception:

   .. code:: python

       raise_(Exception('foo'))

   You can of course also pass an exception type instead of an
   exception instance as the first argument to ``raise_``.

2. Raising an exception with a traceback:

   .. code:: python

       raise_(Exception('foo'), my_traceback_object)


Portability
-----------

Portable to all releases of both Python 3 and Python 2.

(The oldest tested is 2.5, but it will likely work on all Python 2
versions and probably on even earlier versions.)

For implementations of Python that do not support raising with a custom
traceback, a "no traceback" variant can be installed manually.


Advanced/Manual Installation
----------------------------

There are three recommended ways of installing this manually, depending
on your needs:

1. If you're installing it into the library path for your Python system
   as a whole or adding it into the source tree of a project that is
   not meant to be compatible to both Python 3 and Python 2 or older,
   you can just take either ``raise3.py`` or ``raise2.py`` and save it
   *as* ``raise_.py``.

2. If you're adding it into the source tree of a project that should
   work with both Python 3 and Python 2 and older, copy the whole
   ``raise_`` directory.

3. If you're using a Python implementation that does not support raising
   exceptions with a custom traceback, take the ``raise_no_traceback.py``
   file and save it *as* ``raise_.py``.

All of these methods have the advantage that your code can just do
``from raise_ import raise_`` and it'll just work consistently,
without version-detecting boilerplate or hardcoding the version number
in the module name (which is an implementation detail).

You are of course welcome to just copy-paste the tiny ``raise_``
function definition into your code, just keep in mind the compatibility
issues involved: your code will only work without modification on Python
versions compatible with the version you chose, and Python 2's version
causes a SyntaxError in Python 3, which is uncatchable within the same
file.


Design Decisions
----------------

* Allow ``exception`` to be either an instance or a type, because this
  convention is *very* ingrained in Python.

* Do not currently implement an equivalent to Python 3's ``except
  ... from ...`` syntax.

  Ultimately, this syntax just assigns one exception as an attribute
  on another exception.

  This strikes me as *complecting* two different jobs together: raising an
  exception instance and *initializing* an exception instance with a
  ``__cause__`` attribute.

  I note that generators' ``throw`` method does not have support for
  a separe "from"/"cause" argument either. Perhaps it should, but then
  everything implementing this interface would have to implement extra
  logic to handle that extra argument.

  Instead I would advocate for a separate interface for setting the
  ``__cause__`` or ``__context__`` attributes on exceptions.

* Do not use the convention of taking separate ``type`` and ``value``
  arguments because it seems like a counter-intuitive and inappropriate
  convention for *raising* an exception.
  
  Python 3 dropped support for separate ``type`` and ``value`` from the
  ``raise`` statement, so it seems enough people responsible for the
  language already agree with this assessment.

  Also fully/properly supporting all semantics/variations that ``raise``
  allowed before Python 3 would bloat the code excessively.

* Do not support Python 3's ``__traceback__`` behavior: we do not try
  to emulate it in Python 2 and we intentionally suppress Python 3's
  automatic implicit use of ``__traceback__`` when raising, because:

  * When an insufficiently careful coder (almost all of us almost all
    of the time) has code work one way on one platform, they assume it
    will work that way consistently on other platforms.

  * Emulating Python 3's behavior on Python 2 creates extra potential
    for **wrong** behavior: a native ``except`` called between code
    that uses the emulation will result in references to stale traceback
    objects on the exception being used.

  * The following two mantras feel like useful heuristics here:

      Perfection is reached not when there's nothing left to add, but
      when there is nothing left to take away.

    and

      It is far easier to introduce a feature than to remove one.

  * I want to emphasize this again because it's a lesson I learned from
    the portability hellscapes of Bourne shell and C: if it differs
    among implementations it *will be* the source of bugs and pain.

* Using two separate implementation files and an ``__init__.py`` that
  imports one or the other avoids using ``exec``.

  I want to avoid using ``exec`` because

  1. nesting code in strings makes the code less readable and harder to
     consciously verify, *and*

  2. I wanted the implementations for each version of the language to
     be *independently* reusable from a trivial copy-paste.

* Using a ``raise_`` package directory and ``__init__.py`` because it
  makes ``setup.py`` and pip install stupid simple rather than trying
  to figure out a way to only install the right file as ``raise_.py``.

  While I would *love* to implement it so that a ``pip install`` from
  Python 3 only installed ``raise3.py`` as ``raise_.py``, ditto for 2,
  this would make the packaging stuff far less trivial.

* ``__init__.py`` tries ``BaseException.with_traceback`` and uses
  ``NameError`` and ``AttributeError`` to fail instead of ``import
  raise_.raise2`` and ``SyntaxError`` to fail because it conceptually
  highlights the primacy of Python 3 as the ought-to-be-default case.

  I also think it's *conceptually* cleaner to *not* first parse and
  interpret a file only to abort on a syntax error. Performance-wise
  it's negligible and thus a non-issue though.

  Sadly this breaks ``pylint`` on Python 3, because it unconditionally
  imports the `raise2` and aborts upon getting the syntax error. But on
  a tiny module like this, that's not a major issue. I manually worked
  around it to run ``pylint`` by commenting out the offending import,
  and I don't foresee enough changes to make that a hassle.

* We don't do anything about ``flake8`` complaining that ``__version__``
  is imported but not used because this module is too tiny for me to
  justify throwing in some linter-specific disabling comment just to
  quell one spurious warning in an otherwise ``flake8``-silent file.

* Not allowing ``exception`` or ``traceback`` to be arbitrary callables:
  Even though it has value for all/most arguments of all/many functions,
  it is precisely because of this that it is best implemented as a
  general composable tool (such a as a decorator/wrapper function).

  If done, it ought to be done for both exception and traceback, so not
  supporting it for one implies not supporting it for the other.

  Not supporting it is reason to not accidentally let it work despite
  being undocumented, because again, people assume that if it works it
  is supported.

  This is why the code uses an affirmative result from ``issubtype``
  to decide whether to call ``exception`` to construct an instance,
  instead of any other approach, even though this forces calling
  ``isinstance`` first to avoid a spurious ``TypeError``.

* To aid portability of code to Python implementations that do not
  support specifying a custom traceback when raising, allowing
  ``traceback`` to be silently accepted but ignored helps writing code
  that portably follows "progressive enhancement" or "graceful
  degradation" practices: tracebacks are properly used where possible,
  but ignored where not.

  This is **not** always the wisest choice: some features and behavior
  are relied on for security, correctness, or debugging, and in those
  cases the inability to fulfill the contract of an interface must not
  be silently hidden.

  Because of this, the "no traceback" variant is "opt-in": if you're
  using it, you deliberately included it into your project, or a
  dependency of yours did.

* Null out *both* arguments in the ``finally`` inside of ``raise_``
  to alleviate the potential for reference cycles being made by the
  traceback, which references all locals in each stack frame.

  ``traceback`` is obvious: it will cyclically reference itself.

  ``exception`` **might** reference ``traceback`` either directly or
  indirectly, and we have no way to know for sure that it doesn't.

* Not nulling out the arguments to ``raise_`` in the "no traceback"
  variant because the reference cycle depends on having a reference
  to the traceback data within the call stack itself.

  Also, Python implementations that need the "no traceback" variant
  tend to be diversely incompatible: even ``try``-``finally`` does
  not work in all of them.

  So it seems like the "no traceback" variant doesn't need this fix,
  and it is a safer bet to not mess with it until a need is found.


Scope
-----

This package provides the *bare minimum* needed to support the
"``raise`` as a function" approach *portably* and *correctly*.

In particular, Python syntax for raising an exception with
a custom traceback is simply incompatible between Python 3
and Python 2, and the only way around it is **both**

1. separate importable files *or* ``eval``, and
2. catching syntax errors *or* version checking.

So code belongs in here if it protects users from having to code
workarounds at least approximately that bad, for problems that
cannot be better solved by a different design or library.

Everything beyond that is probably out-of-scope.
