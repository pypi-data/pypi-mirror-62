lieparse Python project
=======================

**lieparse** is HTML parser ant text retriever using user defined rule set.

**HISTORY**
-----------

Library was initially written for Vilnius University **Liepa-2** project. Although *LIEPA* is an abbreviation of project name, in Lithuanian *Liepa* means "Linden tree". The tree image is in projects logotype also.

**QUICK USAGE**
---------------

Lets say you have HTML markup text read into string HtmlText.
Then to retrieve all text from division with id="main" you need to::

    from lieparse import lieParser
    rules = '<div id="main">$Data[]</div> ::$Data[];'
    parser = lieParser(rules)
    parser.feed(HtmlText)
    parser.close()

*More sophisticated example can be found after rules syntax definitions*

**RULES SYNTAX**
----------------

Rules consist of statements optionally separated by white space.

White space is considered space, tab, new line and comment.

Comment begins from ``#`` sign and lasts to line end. (Concretely regex match ``r'(?:\s*(?:#.*?\n)?)*\s*'``)

Statements can contain incorporated statements and data definitions.

**Statements are**:
~~~~~~~~~~~~~~~~~~~

**Rep statement**
+++++++++++++++++

loops matching all incorporated statements::

   #(<<other statements>>)
   #+(<<other statements>>)
   *(<<other statements>>)

where::

   # is optional numeric value and means repeat count
   + is one-or-more modifier. If standing alone it is the same as 1+
   * is zero-or-more modifier. Cannot be preceded by number

If ``*`` modifier was specified or when ``+`` modified statement reaches zero count, statement exits on first match of logical statements following *Rep* construct (or of course after enclosing *Tag* ends). In version 1.1.x such *Break* statement has higher priority than internal *Rep* statements. Earlier if same statement matched as *Rep* or as *Break* it was considered as a part of *Rep* statement.

If number or ``+``, ``*`` modifiers are found before other statements (*Tag* or *Any*), repeat block is generated automatically. So writing ``'2<div></div>'`` is automatically converted to ``'2(<div></div>)'``.

**Any statement**
+++++++++++++++++

matches any of incorporated statements::

    {<<other statements>>}

Any-match is done by statements definition order until first one matches. Statement can contain *Any*, *Tag* or *Rep* statements. *Print* statement is not allowed here.

**Tag statement**
+++++++++++++++++

main matching statement the html text is checked onto::

    <name attr="string" $aData[<<aData attrs>>] >
        <<filterStr>> $Data[<<Data attrs>>] <<other statements>>
    </name>

where::

   name is tag name, something like 'div', 'li', 'span'.

   attr is optional and optionally multiple attribute that must be present in html
      tag to be matched. Real tag must contain all, but maybe not only, specified attributes
      to match this rule. If attribute in html tag has no value, in rule it must be
      specified with empty string as a value.

   class="" attribute is split by whitespace into sets while parsing rule as well
      as while parsing html. Rule attribute set must be html attribute subset to match.

   style="" attribute is handled similarly, but splitting on ';' and replacing
      multiple white space to single space and stripping spaces before adding to set.

   $aData is optional and optionally multiple attribute data definition. Can be
      indirect data ($*data[]) also. Definition follows. Data variable name must
      insensitive match regular expression ``'[a-z]+[a-z0-9_]*'``

   filterStr is optional tag data filtering string. If enclosed in '/' marks -
      regular expression match is performed against Tag data. If simple string -
      full match is performed (i.e. "My data" is equivalent to "/^My data$/").
      If tag data is not matched - tag is considered not matching.

   $Data is optional and optionally multiple data collection attribute. Can be
      indirect data ($*data[]) or to-first-tag data ($data[!]) or both.

Statement can incorporate other statements (*Rep*, *Any*, *Tag*, *Print*) mixed with *$Data* definitions

**Print statement**
+++++++++++++++++++

only facility to output gathered data::

    :<<flags>> <<loopDef>>:<<"string">> $pData[<<pData attrs>>] <<Other print statements>> ;

where::

   flags is optional print behavior modifiers - string (no quotes) containing one or
      more flag letters. Next flags are defined:

      n - print new line after full print statement
      N - print new line after each individual loop of print statement
      s - separate each print value with space
      U - convert output to UPERCASE
      u - capitalize output words
      l - convert output to lowercase
      A - redirect output to stream A, can be specified, defaults to sys/stdout
      B - redirect output to stream B, can be specified, defaults to sys/stdout
      C - redirect output to stream C, can be specified, defaults to sys/stdout
        stream parameters are spread to child items but child item can have stream redefined

   loopDef is expression defining how much times print body will be performed. If not
      specified it defaults to 1. If defined - it is counted at run time depending
      on real data. Loop counter is from 0 up-to loopDef. On run time current loop counter
      can be accessed in index expressions as $0. Outer loop statements counter is
      accessible as $1 for first surrounding print statement, $2 for second and so on, the
      last being ourselves (so same as $0).

   loopDef can be one of next:

      indexExpr - countable expression (look below) with $# as surrounding
         loop counters, numbers, parenthesis, arithmetic operations '+', '-', '*'
         and (form version 1.1.0) C-style ternary operators.

      empty - index is set to 1

   string is optional string that will be printed

   pData is data variable name (can be indirect: $*pData) from which data will be printed.
      Full definition is below.

string, pData and other print statements can be freely mixed inside print statement body.

**Index Expressions**
+++++++++++++++++++++

**indexExpr** - countable expression, that can be used in print statement loop definition and in pData (print statement data) definition. It is countable expression with $# as surrounding loop counters, $<<name>> or $*<<name>> as variable array length, numbers, parenthesis and arithmetic operations ``+``, ``-``, ``*``.

**Valid indexExpr's:**

::

   3
   $2 + 1
   ($1 + 1) * 2
   $Data - 1

**Data Definitions**
+++++++++++++++++++++

**Data** definitions can be found inside *Tag* definition (aData), inside *Tag* body (dData and xData) and print statement (pData). Data reference (without []) can be found in print loopDef.

*pData* can not be modified - information is only retrieved from named variable. Other types of Data is dedicated to collect data from tag attributes or html text.

All data variables are arrays. After definition (even if it occurs with ``+`` sign) array pointer is 0. Pointer can be incremented by ``+`` sign in variable attributes. Pointer can never be decremented. ``-`` sign in attributes clears variable data, leaving index unchanged.

``!`` in attributes defines xData instead of dData.

Variables can be direct:

``$<<name>>[<<attr>>]`` - defines variable named <<name>>

and indirect:

``$*<<name>>[<<attr>>]`` - here name of variable is kept in last element of array ``$<<name>>[]``

Only one level of indirection is allowed.

*<<attr>>* and behavior differs depending on variable scope (aData, dData, xData or pData). However in all scopes accessed data is same for same named variable.

*For aData, dData and xData*:
+++++++++++++++++++++++++++++

*<<attr>>* consists of optional flag with values ``!``, ``+`` or ``-`` and optional space separated strings.

If flag is::

   '!' - xData type variable is defined. Valid only for variables inside Tag body.

   '+' - index value is incremented before other operations. The exception is if variable is
         first time defined - in this case index is left 0.

   '-' - all data accumulated in variable by current index is cleared before other operations.

| When no flag is present, data is appended to variable by current index.
| String can be enclosed in double quotation marks. This allows strings with spaces. If no strings are defined - passed data is simply added to variable.

String can be::

   /<<match>>/         - if passed data not matches regular expression it is ignored.
         All other strings are not processed

   /<<find>>/<<repl>>/ - if <<find>> regular expression matches passed data, it is
         replaced with <<repl>> and got data added to variable. On no match - data is
         ignored. Other strings are processed with all data passed to them.

   +/<<find>>/<<repl>>/ - if <<find>> regular expression matches passed data, it is
         replaced with <<repl>> and got data added to variable. On no match - original
         data is added to variable. Always must be enclosed in quotation marks. New in 1.1.0.
         After replace other processing strings (if any) get replaced, not original data.

   @<<attrName>>       - Value of specified Tag attribute is added to variable.

   <<otherString>>     - specified string is added to variable.

*Data passed to variables is*::

   aData - all Tag attributes with names as name="value". If there is some class values
         they are passed as separate class="value" pairs.

   dData - all accumulated data in this and above Tag levels.

   xData - all accumulated data up to first sub-tag match.

*For pData*
+++++++++++
*<<attr>>* can be one of next forms:

``<<indexExpr0>>;<<indexExpr>> <<regexps>>``  - for indirect variables only

or

``<<indexExpr>> <<regexps>>``                - for all variables

where::

   <<indexExpr>> - is optional array index value at which will be printed. If not specified
         defaults to $0

   <<indexExpr0>> - is optional parent array index from which variable name is taken.
         Defaults to $0.

   <<regexps>> is optional regular expressions in form /<<find>>/<<repl>>/
         All expressions are applied to data value before print by order of appearance.

**SYSTEM VARIABLES**
--------------------

From version 1.1.0 we have defined some global system variables. If found anywhere in text variable
name is replaced with it's value. You can use command line (or #!flags) option --no-vars-expand
if such behavior is undesirable. Another workaround is shown in example lieparse3_rule.txt
based on extracting data from this chapter.

*Defined system variables*::

   $URL       -  full URL of site we are examining
   $PROTO     -  protocol of site (http:// or https://)
   $BASEURL   -  base URL of site
   $BASEURLNP -  base URL of site without port number. If no port specified - same as $BASEURL
   $PORT      -  port number. If not specified, empty string
   $DATE      -  date the extracting program is being run (as returned by strftime("%x"))
   $TIME      -  time, program is running (as returned by strftime("%X"))
   $DATETIME  -  date and time, program is running (as returned by strftime("%c"))

**Parsing parameters inside rules file**
----------------------------------------

|
| Starting with version 1.1.0 you can define parsing parameters inside rules file.
| Older versions treats this as comment.

Syntax is: ``#!<<parameter name>> <<space separated parameter values>>``

Do not define parameters in first file line - Linux shell will treat that as executable file definition.

Next parameters are recognized::

   url      -  location to parse URL
   href     -  same as above. If both specified, first found is used
   winurl   -  URL for Windows systems. Normally used with file:// references
   winhref  -  same as above
   linurl   -  URL for Linux systems. Normally used with file:// references
   linhref  -  same as above
   usragent -  user agent. Can be specified by name or by value
   fromurl  -  set URL we are coming from
   flags    -  specify list of space separated behavior flags. Next are defined:
      ssl-verify, dump-rules, dump-vars, dump-json, dump-json-np, no-vars-expand
   output-file[ABCE]? see LiepaParse -h for definition
   time-locale - specify locale for system time variables $DATE, $DATETIME and $TIME


**ADVANCED EXAMPLE**
--------------------

We will retrieve python library names from docs.python.org site::

    import sys
    from lieparse import lieParser
    from pycurl import Curl, global_init, global_cleanup, GLOBAL_ALL
    usragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"
    url = "https://docs.python.org/3.6/py-modindex.html"
    rules = r'''
    <table class="indextable modindextable">
        *<code class="xref">
            $Data[+]
        </code>
    </table>
    :N $Data:$Data[];     # if flags are ns we will have space separated list
    '''

    global_init(pycurl.GLOBAL_ALL)
    c = Curl()
    c.setopt(c.USERAGENT, usragent)
    c.setopt(c.SSL_VERIFYPEER, 0)      # have problems verifying certificate under Windows
    c.setopt(c.URL, url)
    s = c.perform_rs()
    global_cleanup()

    parser = lieParser(rules)
    parser.feed(s)
    v = parser.close()
    if v != 0:
        print("Unmatched {} items".format(v), file=sys.stderr)

**Summary**
-----------

:Author: Vidmantas Balčytis <vidma@lema.lt>
:Version: 1.1.0 (2020-03-03)
:Changes: 1.0.0- 1.0.4 versions released have same code base and differs only in documentation

          1.0.5
            - bug fix looping all rules after full match
            - bug fix retrieving attribute data
            - syntax and value error no more prints traceback
            - added testing script LiepaParse and samples

          1.1.0 major service release, compatible with rules written for older versions.
            - breaking statement from zero-or-more *Rep* loop has now greater priority than internal `Rep statement`_. thats why some rules written for 1.1.x may not run on 1.0.x. Backwards compatibility is ensured.
            - `Index Expressions`_ now can have $<<var name>> and $*<<var name>> as operands. Also C-style ternary operations were added.
            - `Print statement`_ new flags are introduced
            - formating now is preserved in <pre> tags
            - `SYSTEM VARIABLES`_ and their expansion is introduced
            - added find/replace string with keep-on-not-found type in data variables.
            - `Parsing parameters inside rules file`_ is introduced.
