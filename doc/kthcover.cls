\NeedsTeXFormat{LaTeX2e}[95/06/01]
\ProvidesClass{kthcover}
              [1999/04/16 Document class for KTH theses, version 0.9]
\newcommand\@ptsize{10}
\newif\if@mainmatter \@mainmatterfalse
\newif\if@openright  \@openrighttrue
\newif\if@onlyinsert \@onlyinsertfalse
\newif\if@swedishabstract \@swedishabstractfalse
\@twosidefalse
\DeclareOption{g5paper}%
   {\setlength\paperheight {239mm}%
    \setlength\paperwidth  {169mm}%
    \setlength\textheight  {43pc}%
    \setlength\textwidth   {30pc}}
\DeclareOption{s5paper}%
   {\setlength\paperheight {242mm}%
    \setlength\paperwidth  {165mm}%
    \setlength\textheight  {44pc}%
    \setlength\textwidth   {29pc}}
\DeclareOption{a4paper}%
   {\setlength\paperheight {297mm}%
    \setlength\paperwidth  {210mm}%
    \setlength\textheight  {49pc}%
    \setlength\textwidth   {33pc}}
\DeclareOption{9pt}{\renewcommand\@ptsize{9}}
\DeclareOption{10pt}{\renewcommand\@ptsize{10}}
\DeclareOption{11pt}{\renewcommand\@ptsize{11}}
\DeclareOption{12pt}{\renewcommand\@ptsize{12}}
\DeclareOption{draft}{\setlength\overfullrule{5pt}}
\DeclareOption{final}{\setlength\overfullrule{0pt}}
\ExecuteOptions{s5paper,10pt,final}
\ProcessOptions
\RequirePackage{graphics}
\if@swedishabstract\RequirePackage[swedish,english]{babel}\fi
\input{kthbk\@ptsize.clo}
\input{fleqn.clo}
\setlength\lineskip{1\p@}
\setlength\normallineskip{1\p@}
\renewcommand\baselinestretch{}
\setlength\parskip{0\p@ \@plus \p@}
\@lowpenalty   51
\@medpenalty  151
\@highpenalty 301
\clubpenalty=9996
\widowpenalty=9999
\brokenpenalty=4991
\predisplaypenalty=10000
\postdisplaypenalty=1549
\displaywidowpenalty=1602
\def\title#1{\ifx#1[\let\next\@bracket@title\else%
  \gdef\@title{#1}\gdef\@shorttitle{\@title}\let\next\relax\fi\next}
\def\@bracket@title#1]#2{\gdef\@shorttitle{#1}\gdef\@title{#2}}
\def\author#1{\ifx#1[\@bracket@author\else%
  \gdef\@author{#1}\gdef\@shortauthor{\@author}\fi}
\def\@bracket@author#1]#2{\gdef\@shortauthor{#1}\gdef\@author{#2}}
\def\type#1{\gdef\@type{#1}}
\def\comment#1{\gdef\@comment{#1}}
\def\department#1{\gdef\@department{#1}}
\def\address#1{\gdef\@address{#1}}
\def\imprint#1{\gdef\@imprint{#1}}
\def\publisher#1{\gdef\@publisher{#1}}
\def\trita#1{\gdef\@trita{#1}}
\def\issn#1{\gdef\@issn{#1}}
\def\isrn#1{\gdef\@isrn{#1}}
\def\isbn#1{\@isbntrue \gdef\@isbn{#1}}
\def\dedication#1{\@dedicationtrue \gdef\@dedication{#1}}
\newif\if@isbn \@isbnfalse
\newif\if@dedication \@dedicationfalse
\def\@shortauthor{\@author}
\def\@shorttitle{\@title}
\def\@type{\@latex@warning{No report type given}}
\def\@comment{\relax}
\def\@imprint{\@latex@warning{No imprint given}}
\def\@institute{Royal Institute of Technology}
\def\@department{\@latex@warning{No department given}}
\def\@address{\@latex@warning{No address to the author given}}
\def\@publisher{\@latex@warning{No publisher given}}
\def\@trita{\@latex@warning{No TRITA number given}}
\def\@issn{\@latex@warning{No ISSN given}}
\def\@isrn{\@latex@warning{No ISRN given}}
\let\thanks\empty
\newcommand\@make@title@page{%
  \noindent%
  \kern6mm%
  \vbox to 5mm{\hbox{\includegraphics{kthtext.eps}}\vss}%
  \hfill%
  \if@isbn\else%
  \vbox to 0mm{\footnotesize
      \hbox to 0mm{\hss TRITA-\@trita}
      \hbox to 0mm{\hss ISSN~\@issn}
      \hbox to 0mm{\hss ISRN~\@isrn}\vss}%
  \kern4mm%
  \fi\par
  \vskip 180\p@
  \begin{center}
  \begin{minipage}{29pc}
  \begin{center}%
    {\LARGE \@title \par}%
    \vskip 3em%
    {\Large
      \lineskip .75em%
      \begin{tabular}[t]{c}%
        \@author
      \end{tabular}\par}%
  \end{center}\par
  \end{minipage}
    \vfill%
  \begin{minipage}{29pc}
  \begin{center}%
    {\large \@imprint \par}
    \vskip 1em%
    {\large
      \lineskip .75em%
      \begin{tabular}[t]{c}%
        \@type \\ \@institute \\ \@department
      \end{tabular}\par}%
  \end{center}\par
  \end{minipage}
  \end{center}
\setcounter{footnote}{0}}
\newcommand\@maketitle{%
  \cleardoublepage
  \@make@title@page
  \clearpage
  \begingroup
  \voffset=-1in
  \topskip=-1in
  \topmargin=0pt
  \headsep=0pt
  \headheight=0pt
  \footskip=0pt
  \rotatebox{-90}{%
    \rlap{\hbox to \paperheight{\large\bfseries%
        \hbox to 4.5cm{\kern0.5cm\@shortauthor\hfil\kern0.5cm}%
        \kern0.5cm{\itshape\@shorttitle}\hfil\kern5.5cm}}}
  \clearpage
  \endgroup
  \vglue 0pt plus 1fill
  \footnotesize
  \if@isbn
  \noindent%
  ISBN~\@isbn \\[\smallskipamount]
  TRITA-\@trita \\
  ISSN~\@issn \\
  ISRN~\@isrn\par\smallskip
  \fi
  \bigskip\noindent\@address\par
  \clearpage
  \global\let\@maketitle\relax
  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\type\relax
  \global\let\comment\relax
  \global\let\department\relax
  \global\let\address\relax
  \global\let\imprint\relax
  \global\let\publisher\relax
  \global\let\trita\relax
  \global\let\issn\relax
  \global\let\isrn\relax
  \global\let\isbn\relax
  \global\let\dedication\relax
  \global\let\and\relax
}
\AtBeginDocument{\@maketitle}
\newcommand*\chaptermark[1]{}
\setcounter{secnumdepth}{2}
\newcounter {part}
\newcounter {chapter}
\newcounter {section}[chapter]
\newcounter {subsection}[section]
\newcounter {subsubsection}[subsection]
\newcounter {paragraph}[subsubsection]
\newcounter {subparagraph}[paragraph]
\renewcommand \thepart {\@Roman\c@part}
\renewcommand \thechapter {\@arabic\c@chapter}
\renewcommand \thesection {\thechapter.\@arabic\c@section}
\renewcommand\thesubsection   {\thesection.\@arabic\c@subsection}
\renewcommand\thesubsubsection{\thesubsection .\@arabic\c@subsubsection}
\renewcommand\theparagraph    {\thesubsubsection.\@arabic\c@paragraph}
\renewcommand\thesubparagraph {\theparagraph.\@arabic\c@subparagraph}
\newcommand\@chapapp{\chaptername}
\setlength\leftmargini  {2.5em}
\leftmargin  \leftmargini
\setlength\leftmarginii  {2.2em}
\setlength\leftmarginiii {1.87em}
\setlength\leftmarginiv  {1.7em}
\setlength\leftmarginv  {1em}
\setlength\leftmarginvi {1em}
\setlength  \labelsep  {.5em}
\setlength  \labelwidth{\leftmargini}
\addtolength\labelwidth{-\labelsep}
\@beginparpenalty -\@lowpenalty
\@endparpenalty   -\@lowpenalty
\@itempenalty     -\@lowpenalty
\renewcommand\theenumi{\@arabic\c@enumi}
\renewcommand\theenumii{\@alph\c@enumii}
\renewcommand\theenumiii{\@roman\c@enumiii}
\renewcommand\theenumiv{\@Alph\c@enumiv}
\newcommand\labelenumi{\theenumi.}
\newcommand\labelenumii{(\theenumii)}
\newcommand\labelenumiii{\theenumiii.}
\newcommand\labelenumiv{\theenumiv.}
\renewcommand\p@enumii{\theenumi}
\renewcommand\p@enumiii{\theenumi(\theenumii)}
\renewcommand\p@enumiv{\p@enumiii\theenumiii}
\newcommand\labelitemi{\textbullet}
\newcommand\labelitemii{\normalfont\bfseries \textendash}
\newcommand\labelitemiii{\textasteriskcentered}
\newcommand\labelitemiv{\textperiodcentered}
\newenvironment{description}
               {\list{}{\labelwidth\z@ \itemindent-\leftmargin
                        \let\makelabel\descriptionlabel}}
               {\endlist}
\newcommand*\descriptionlabel[1]{\hspace\labelsep
                                \normalfont\bfseries #1}
\newenvironment{verse}
               {\let\\\@centercr
                \list{}{\itemsep      \z@
                        \itemindent   -1.5em%
                        \listparindent\itemindent
                        \rightmargin  \leftmargin
                        \advance\leftmargin 1.5em}%
                \item\relax}
               {\endlist}
\newenvironment{quotation}
               {\list{}{\listparindent 1.5em%
                        \itemindent    \listparindent
                        \rightmargin   \leftmargin
                        \parsep        \z@ \@plus\p@}%
                \item\relax}
               {\endlist}
\newenvironment{quote}
               {\list{}{\rightmargin\leftmargin}%
                \item\relax}
               {\endlist}
\DeclareOldFontCommand{\rm}{\normalfont\rmfamily}{\mathrm}
\DeclareOldFontCommand{\sf}{\normalfont\sffamily}{\mathsf}
\DeclareOldFontCommand{\tt}{\normalfont\ttfamily}{\mathtt}
\DeclareOldFontCommand{\bf}{\normalfont\bfseries}{\mathbf}
\DeclareOldFontCommand{\it}{\normalfont\itshape}{\mathit}
\DeclareOldFontCommand{\sl}{\normalfont\slshape}{\@nomath\sl}
\DeclareOldFontCommand{\sc}{\normalfont\scshape}{\@nomath\sc}
\DeclareRobustCommand*\cal{\@fontswitch\relax\mathcal}
\DeclareRobustCommand*\mit{\@fontswitch\relax\mathnormal}
\newcommand\abstractname{Abstract}
\newcommand\contentsname{Contents}
\newcommand\listfigurename{List of Figures}
\newcommand\listtablename{List of Tables}
\newcommand\bibname{Bibliography}
\newcommand\indexname{Index}
\newcommand\figurename{Figure}
\newcommand\tablename{Table}
\newcommand\partname{Part}
\newcommand\chaptername{Chapter}
\newcommand\appendixname{Appendix}
\newcommand\today{}
\edef\today{\ifcase\month\or
  January\or February\or March\or April\or May\or June\or
  July\or August\or September\or October\or November\or December\fi
  \space\number\day, \number\year}
\onecolumn
\pagenumbering{roman}
\pagestyle{empty}
\endinput
