\NeedsTeXFormat{LaTeX2e}

\ProvidesClass{GeM-UPM}  %[2025-03-04]

% Clase libro
\LoadClass[12pt,a4paper,twoside]{book}

\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Idioma
%
\RequirePackage[spanish,es-tabla,es-ucroman]{babel}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Valores "constantes"
%
\def\universityname{Universidad Politécnica de Madrid}
\def\templaterepository{https://github.com/blazaid/UPM-Report-Template}
\def\degree{Grado en Matemáticas e Informática}
\def\typeofreport{Trabajo Final Modelización}
\def\school{Escuela Técnica Superior de Ingenieros Informáticos}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Opciones de la plantilla
\RequirePackage{kvoptions}

% Las opciones que declaremos a continuación tendrán el prefijo upm@. Si son booleanas, crearán el \ifupm@code, \ifupm@index, etc.
\SetupKeyvalOptions{
    family = upm, 
    prefix = upm@
}

% Es una opción para la plantilla si usa código o no
% En ambos, por defecto, tiene a falso como valor inicial
\DeclareBoolOption{code}% Opción si contiene código
\DeclareBoolOption{index}% Opción de si queremos el índice alfabético de términos
\DeclareBoolOption{nonCC}% Opción de eliminar el Creative Commons
% \DeclareBoolOption{biblatex}% Opción para cargar biblatex
\DeclareStringOption[false]{biblatex}[alphabetic]

% Esto activa todas las opciones que hemos definido anteriormente
\ProcessKeyvalOptions*


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Paquetes globales
%
\RequirePackage[naturalnames]{hyperref} % Esencial para los enlaces internos y externos del PDF
\RequirePackage{changepage}  % Para poder usar los adjustwidth
\RequirePackage{etoolbox}  % Condicionales
\RequirePackage{graphicx}  % Mejoras sobre el paquete graphics
\RequirePackage[x11names]{xcolor}  % Mejoras sobre el paquete color
\RequirePackage[titletoc]{appendix}  % Que aparezca "Apéndice"
\RequirePackage{eso-pic}  % Colores y fondos
\RequirePackage{hologo}  % Para poner logos relacionados con LaTeX
\RequirePackage{lipsum}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Logos y colores corporativos

\newcommand{\schoollogo}{logos/logo-epes-dark.png}
\definecolor{schoolcolor}{cmyk}{1.0, 0.78, 0.0, 0.18}
\definecolor{linkcolor}{cmyk}{1.0, 0.78, 0.0, 0.18}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Minted package
%
\makeatletter
\ifupm@code% Carga únicamente cuando la opción code está activada
%\RequirePackage[cache=false]{minted}
\RequirePackage{minted}

% Paleta de colores
\usemintedstyle{autumn}%trac, vim, inkpot, autumn, gruvbox-light, xcode, vs, friendly, rainbow_dash, emacs

% Código para que las listas incluyan el número de capítulo, y homogeneizarlo con las tablas y las figuras.
\renewcommand*{\thelisting}{\thechapter.\arabic{listing}}
\@addtoreset{listing}{chapter}
\else
% \iftotallistings tiene que ser condicional incluso cuando la opción code no está activada. De lo contrario el condicional anidado del índice de códigos no empareja correctamente cuando la opción code está desactivada.
\newif\iftotallistings
\totallistingsfalse
\fi
\makeatother
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Variables
%
\makeatletter
\newcommand{\bibauthor}[1]{\gdef\@bibauthor{#1}}%
\newcommand{\@bibauthor}{\@latex@warning@no@line{No \noexpand\bibauthor given}}
\newcommand{\genderauthor}[1]{\gdef\@genderauthor{#1}}
\newcommand{\@genderauthor}{\@latex@warning@no@line{No \noexpand\genderauthor given}}
\newcommand{\tutor}[1]{\gdef\@tutor{#1}}%
\newcommand{\@tutor}{\@latex@warning@no@line{No \noexpand\tutor given}}
\newcommand{\bibtutor}[1]{\gdef\@bibtutor{#1}}%
\newcommand{\@bibtutor}{\@latex@warning@no@line{No \noexpand\bibtutor given}}
\newcommand{\fecha}[1]{\gdef\@fecha{#1}}
\newcommand{\@fecha}{\@date}
\makeatother
% Convertir en 'y' el 'and'
%
\renewcommand{\and}{y\space}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Geometría general de las páginas
%
\RequirePackage[a4paper]{geometry}
% Versión en papel
%\geometry{textwidth=14cm, textheight=21.3cm, marginratio={4:6,5:6}}
% Versión electrónica
\geometry{textwidth=14cm, textheight=21.3cm, marginratio={1:1,5:6}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Cabeceras y pies de página
%
\RequirePackage{fancyhdr}
\RequirePackage{emptypage}
\setlength{\headheight}{15.8pt}
\pagestyle{fancy}

% Cambiamos el color de la línea de cabecera
\let\oldheadrule\headrule% Copy \headrule into \oldheadrule
\renewcommand{\headrule}{\color{schoolcolor}\oldheadrule}% Add colour to \headrule
% Estilos globales
\fancyhf{}

% Estilos para páginas impares
\fancyhead[LO]{\textcolor{schoolcolor}{\sffamily\nouppercase{\leftmark}}}
\fancyhead[RO]{\textcolor{schoolcolor}{\sffamily\thepage}}

% Estilos para páginas pares
\fancyhead[RE]{\textcolor{schoolcolor}{\sffamily\nouppercase{\rightmark}}}
\fancyhead[LE]{\textcolor{schoolcolor}{\sffamily\thepage}}

\renewcommand{\headrulewidth}{0.5pt}
% Eliminamos la mención de "Capítulo" en las cabeceras
\renewcommand\chaptermark[1]{\markboth{\thechapter.\ #1}{}}

% Estilos en páginas "plain" (e.g. primera de capítulo)
\fancypagestyle{plain}{%
    \fancyhf{}
    \renewcommand{\headrule}{}
    \renewcommand{\footrule}{}
}

% Ponemos el color de la escuela a la línea que separa las notas al pie de página, para ello anteponemos el color a la definición existente de \footnoterule
\makeatletter
\let\aux@footnoterule\footnoterule
\def\footnoterule{%
{\color{schoolcolor}\aux@footnoterule}%
}%
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Estilos de capítulo, sección, ...
%
\RequirePackage{titlesec}

%% El formato de capítulo para el resto
\def\mainchapter{%
\titleformat{\chapter}
    [display]% shape 
    {\sffamily\fontsize{60}{0}\selectfont\bfseries\filright}% Format
    {\hspace{0.6em}\thechapter}% Label
    {12pt}% Shape
    {\color{schoolcolor}\raisebox{-6pt}[0pt]{\rule{0.25em}{8.pc}\hspace{0.3em}}\fontsize{35}{35}\selectfont}% Before code
    % []% After code
    \titlespacing*{\chapter}{0pt}{1.5cm}{25pt}
}

\def\extrachapter{%
\titleformat{\chapter}%
    {\fontsize{30}{30}}%
    {\sffamily\fontsize{30}{30}\color{schoolcolor}\thechapter.}%
    {0.6em}%
    {\sffamily\fontsize{30}{30}\color{schoolcolor}\raggedleft\hspace*{\fill}}
    [\color{schoolcolor}\hrule]
    \titlespacing*{\chapter}{0pt}{0pt}{25pt}
}

\titleformat{\section}%
    {}{\sffamily\huge\color{schoolcolor}\thesection.}{0.6em}{\sffamily\huge\color{schoolcolor}}
\titleformat{\subsection}%
    {}{\sffamily\Large\color{schoolcolor}\thesubsection.}{0.6em}{\sffamily\Large\color{schoolcolor}}
\titleformat{\subsubsection}%
    {}{\sffamily\large\color{schoolcolor}\thesubsubsection.}{0.6em}{\sffamily\large\color{schoolcolor}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Estilos de la tabla de contenidos
%
\RequirePackage{titletoc}
\setcounter{tocdepth}{1}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Fuentes (EB Garamond)
%
\RequirePackage{microtype} % Mejoras tipográficas generales
\RequirePackage{amsmath,amsthm,amssymb}% Paquetes usuales matemáticos
\RequirePackage{mathtools} % Más mejoras de presentación matemática

%% Fuente de palo seco (sans serif)
\usepackage[scale=0.80]{ClearSans}
%% Fuente matemática
\usepackage[cmintegrals,cmbraces]{newtxmath}
%%% Fuente principal del cuerpo del texto (serif)
\usepackage{ebgaramond-maths}
%% Fuente monoespaciada
\usepackage[scaled=0.75]{beramono}

\makeatletter
  \DeclareSymbolFont{ntxletters}{OML}{ntxmi}{m}{it}
  \SetSymbolFont{ntxletters}{bold}{OML}{ntxmi}{b}{it}
  \re@DeclareMathSymbol{\leftharpoonup}{\mathrel}{ntxletters}{"28}
  \re@DeclareMathSymbol{\leftharpoondown}{\mathrel}{ntxletters}{"29}
  \re@DeclareMathSymbol{\rightharpoonup}{\mathrel}{ntxletters}{"2A}
  \re@DeclareMathSymbol{\rightharpoondown}{\mathrel}{ntxletters}{"2B}
  \re@DeclareMathSymbol{\triangleleft}{\mathbin}{ntxletters}{"2F}
  \re@DeclareMathSymbol{\triangleright}{\mathbin}{ntxletters}{"2E}
  \re@DeclareMathSymbol{\partial}{\mathord}{ntxletters}{"40}
  \re@DeclareMathSymbol{\flat}{\mathord}{ntxletters}{"5B}
  \re@DeclareMathSymbol{\natural}{\mathord}{ntxletters}{"5C}
  \re@DeclareMathSymbol{\star}{\mathbin}{ntxletters}{"3F}
  \re@DeclareMathSymbol{\smile}{\mathrel}{ntxletters}{"5E}
  \re@DeclareMathSymbol{\frown}{\mathrel}{ntxletters}{"5F}
  \re@DeclareMathSymbol{\sharp}{\mathord}{ntxletters}{"5D}
  \re@DeclareMathAccent{\vec}{\mathord}{ntxletters}{"7E}
\makeatother



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Configuración de figuras y tablas
%
\RequirePackage{float}      % Mejorar colocación de elementos flotantes
\RequirePackage{tabularx}   % Tablas más configurables
\RequirePackage{booktabs}   % Configuraciones para tablas más bonitas
\RequirePackage{caption}    % Mejora de pies de figuras
\RequirePackage{subcaption} % Pies de subfiguras

% Formato del caption personalizado
\DeclareCaptionFormat{caption-upm}{#1#2~\small #3}
\DeclareCaptionLabelFormat{caption-upm}{\textbf{#1 #2}}
\DeclareCaptionLabelSeparator{caption-upm}{.}

\captionsetup{
    format=caption-upm,
    labelformat=caption-upm,
    labelsep=caption-upm,
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Configuración general de espaciados, geometrías y otros
%
\setlength{\parskip}{0pt}% Al haber sangría, no es necesario el espaciado entre párrafos
\linespread{1.15}% Para cambiar la separación entre líneas sin cambiar el tamaño de la fuente
\setlength{\parindent}{15pt}% Especificación de la sangría en la primera línea de cada párrafo

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Configuración para PDF e hipervínculos
%
\makeatletter
\hypersetup{
    pdfauthor={\@author},
    pdftitle={\@title},
    pdfcreator={\@author},
    pdfproducer={},
    breaklinks=true,
    linktoc=all,
    plainpages=false,
    unicode=true,
    colorlinks=true,
    anchorcolor={linkcolor},
    citecolor={linkcolor},
    linkcolor={linkcolor},
    urlcolor={linkcolor},
}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% % Listados condicionales
% %
\makeatletter
\ifupm@code
\RequirePackage[
    figure,table,listing,equation
    ]{totalcount}  % Contar las veces que aparecen entradas en listados
\else
\RequirePackage[
    figure,table,equation
    ]{totalcount}  % Contar las veces que aparecen entradas en listados
\fi
\makeatother
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Licencia de la memoria
%
\makeatletter
\ifupm@nonCC
% Caso en el que el autor no desea que su trabajo tenga licencia Creative Commons, necesario para publicarlo en el repositorio de la UPM
\newcommand{\licencia}{%
    \vspace*{1em}
    Plantilla derivada de \href{\templaterepository}{\templaterepository}.
    }
\else
% Caso en el que si tiene la licencia Creative Commons 4.0
\RequirePackage[%
    type={CC},%
    modifier={by-nc-sa},%
    version={4.0}%
]{doclicense}
% Impresión de licencia modificada para que incluya más cosas. Es un clon de \docLicenseThis
\newcommand{\licencia}{%
    \setlength{\doclicense@hsize}{\linewidth-\doclicense@imagewidth-\doclicense@imagedistance}%
    \begin{center}
        \begin{minipage}{\doclicense@hsize}
            \ifcsempty{\doclicense@hyphenation}{}{%
                \@nameuse{\doclicense@hyphenation}%
            }%
            \doclicenseLongText\\[1em]
            Plantilla derivada de \href{\templaterepository}{\templaterepository}.%
        \end{minipage}
        \hfill
        \begin{minipage}{\doclicense@imagewidth}\doclicenseImage\end{minipage}
    \end{center}
}
\fi
\makeatother
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Referencias y bibliografía
%
% \RequirePackage[backend=biber, style=alphabetic]{biblatex}
\RequirePackage[debug = true, style = spanish]{csquotes}  % Facilita el trabajo con citas

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Portada
%
\makeatletter         
\renewcommand\maketitle{{
    \sffamily
    \thispagestyle{empty}
    % Barra lateral izquierda y logo fondo
    \AddToShipoutPicture*{%
        \AtPageLowerLeft{%
            \put(90,750){% Logos de las escuelas.
            \lower2ex\hbox{\includegraphics[width=0.30\paperwidth]{logos/logo-upm-horizontal}} \quad
            \includegraphics[width=0.30\paperwidth]{logos/logo-epes}  \quad
            \lower2ex\hbox{
            \includegraphics[width=0.16\paperwidth]{logos/logo-gem}}
            }
            \makebox[1\paperwidth][r]{%
                \includegraphics[width=0.9\paperwidth]{logos/logo-upm}
            }%
        }
        \put(0,0){%
            \colorbox{schoolcolor}{%
                \parbox[b][\paperheight]{2cm}{\vfill\hfill}
            }%
        }
    }
    \vspace*{2em}
    \begin{adjustwidth}{1.5cm}{}% Ajustamos los márgenes de la página
        {\large\MakeUppercase{\universityname}}\\*[0.5em]
        {\large\MakeUppercase{\textbf{\school}}}\\*[0.5em]
        {\large\MakeUppercase{\typeofreport}}\\*[0.5em]
        {\large\MakeUppercase{\textbf{\degree}}}
        \vfill
        \begin{hyphenrules}{nohyphenation}
        \raggedright
        \begin{sloppypar}\fontsize{40}{40}\selectfont\bfseries\@title\end{sloppypar}
        \end{hyphenrules}
        \vfill

        \parbox[b]{\linewidth}{
            \large
            \newbox\advisors@box
            \setbox\advisors@box = \hbox{{\bfseries Dirigido por:}\ }
            {\bfseries Autor\ifdefstring{\@genderauthor}{M}{}{a}:} \@author
            \vspace*{1ex}

            \noindent\leftskip=\wd\advisors@box
            \llap{\copy\advisors@box}\ignorespaces
            \@tutor
            \vspace*{1ex}

            \leftskip=0pt
            Madrid, \@fecha
        }
    \end{adjustwidth}
    \normalfont
    \normalsize
}}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Licencia
%
\makeatletter
\newcommand\makelicense{{
    \footnotesize
    \newbox\advisors@box
    \setbox\advisors@box=\hbox{{\bfseries Dirigido por:}\ }
    \clearpage
    \thispagestyle{empty}
    ~\vfill
    \par{\parskip=0pt\parindent=0pt
        \textit{\@title}\\
        \textbf{Autor\ifdefstring{\@genderauthor}{M}{}{a}:} \@author
        
        \noindent\leftskip=\wd\advisors@box
        \llap{\copy\advisors@box}\ignorespaces\@tutor
        
        \typeofreport, \@fecha\\
    }
    
    \newline
    \hrule
    \vspace*{\baselineskip}
    \par{\parindent=0pt
        Si deseas citar este trabajo, la entrada completa en \hologo{BibTeX} es la siguiente:

        \texttt{%
            @mastersthesis\{citekey,\\
                title   = \{\@title\},\\
                author  = \{\@bibauthor~y~\@bibtutor\},\\
                school  = \{\school\},\\
                year    = \{\the\year\},\\
                type    = \{\typeofreport\}\\
            \}
        }
    }
    \newline
    \hrule
    \par{\licencia}
 }}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Agradecimientos
%
\makeatletter
% Se define los agradecimientos 
\newcommand{\acknowledgements}[1]{\gdef\@acknowledgements{#1}}%
\newcommand{\@acknowledgements}{}
\newcommand\makeacknowledgements{{
    \ifdefstring{\@acknowledgements}{}{}{
        \clearpage
        \thispagestyle{empty}
        \chapter*{Agradecimientos}
        \@acknowledgements
    }
}}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Índice alfabético de términos
%
\makeatletter
\ifupm@index
\RequirePackage{imakeidx}
\makeindex[intoc=true]
\fi
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Bibliografía con biblatex
%
\makeatletter
\ifdefstring{\upm@biblatex}{false}{}{%
\RequirePackage[backend=biber, style=\upm@biblatex]{biblatex}
\addbibresource{referencias.bib}
}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Cubierta trasera
%
\makeatletter         
\newcommand{\makebackcover}{
    \clearpage
    \thispagestyle{empty}
    \newgeometry{hmarginratio={1:1}}% Evita que los márgenes no iguales descentren la figura
    \pagecolor{schoolcolor}
    \AddToShipoutPicture*{%
        \put(0,0){%
            \colorbox{black}{%
                \parbox[b][12cm]{\paperwidth}{\vfill\hfill}
            }%
        }
    }
    \vspace*{\fill}
    \begin{center}
        \includegraphics[width=6cm]{\schoollogo}
    \end{center}
}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Elementos del comienzo del documento
%
\makeatletter
%\AtBeginDocument{%
\AddToHook{begindocument/end}{
    \extrachapter
    \maketitle% Título
    \makelicense% Licencia
    \makeacknowledgements% Agradecimientos (si hay)
    \makeresumen% Resumen
    \makeabstract% Resumen en inglés

    % Comienzo de los índices
    \frontmatter

    \begingroup
        \parskip=0pt% Espaciado entre las líneas del índice
        \tableofcontents
        \begingroup
        % Si hay figuras
        \iftotalfigures
        \listoffigures
        \vspace{3\baselineskip}
        \let\clearpage\relax
        \fi
        % Si hay tablas
        \iftotaltables
        \listoftables
        \vspace{3\baselineskip}
        \let\clearpage\relax
        \fi
        % Si hay códigos
        \ifupm@code
        \iftotallistings
        \listoflistings
        \fi
        \fi
        \endgroup
    \endgroup

    \mainchapter
    \mainmatter
}
\makeatother


\endinput