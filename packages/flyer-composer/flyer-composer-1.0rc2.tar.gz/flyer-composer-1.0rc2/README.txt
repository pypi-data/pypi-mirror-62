==========================
Flyer Composer
==========================

-------------------------------------------------------------
Rearrange PDF pages to print as flyers on one paper
-------------------------------------------------------------

:Author:    Hartmut Goebel <h.goebel@crazy-compilers.com>
:Version:   Version 1.0rc2
:Copyright: 2008-2020 by Hartmut Goebel
:Licence:   GNU Affero General Public License v3 or later (AGPLv3+)
:Homepage:  http://crazy-compilers.com/flyer-composer

`Flyer Composer` can be used to prepare one- or two-sided flyers for
printing on one sheet of paper.

Imagine you have designed a flyer in A6 format and want to print it using your
A4 printer. Of course, you want to print four flyers on each sheet. This is
where `Flyer Composer` steps in, creating a PDF which holds your flyer
four times. If you have a second page, `Flyer Composer` can arrange it
the same way - even if the second page is in a separate PDF file.

This also work if your input file was designed for e.g. A2: it will simply be
scaled down to A6 and placed four times in the sheet. And, of course,  `PDF
Flyer Composer` supports other flyer sizes or paper sizes, too.

This is much like `pdfnup` (or `psnup`), except that the *same* page is
put the paper several times.

`Flyer Composer` contains two programs: a Qt-based GUI one
(`flyer-composer-gui`) and a command line one (`flyer-composer`).

For more information please refer to the manpage or visit
the `project homepage <http://crazy-compilers.com/flyer-composer>`_.


Download
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Flyer Composer` for Windows and Linux can be downloaded from
http://crazy-compilers-com/flyer-composer.


Requirements when Installating from Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to install `Flyer Composer` from source, make sure you have the
following software installed:

* `Python 3`__  (tested with 3.7),
* `setuptools`__ or `pip`__ for installation, and
* `PyPDF2`__.

For the Qt GUI additionally:

* `PyQt5`__ and
* `python-poppler-qt5`__ or `PyMuPDF`__.

For further information please refer to the `Installation instructions
<https://flyer-composer.readthedocs.io/en/latest/Installation.html>`_.

__ https://www.python.org/download/
__ https://pypi.org/project/setuptools
__ https://pypi.org/project/pip
__ http://mstamy2.github.io/PyPDF2/
__ https://pypi.org/project/PyQt5/
__ https://pypi.python.org/pypi/python-poppler-qt5/
__ https://pypi.org/project/PyMuPDF/


.. Emacs config:
 Local Variables:
 mode: rst
 End:
