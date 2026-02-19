from .component import Element


class A(Element):
    """Creates a hyperlink to another page or location."""

    tag = "a"


class Abbr(Element):
    """Represents an abbreviation or acronym."""

    tag = "abbr"


class Address(Element):
    """Provides contact information for a person or organization."""

    tag = "address"


class Area(Element):
    """Defines a clickable area in an image map."""

    tag = "area"


class Article(Element):
    """Represents a self-contained piece of content."""

    tag = "article"


class Aside(Element):
    """Represents content related to surrounding content."""

    tag = "aside"


class Audio(Element):
    """Embeds sound content."""

    tag = "audio"


class B(Element):
    """Draws attention to text without extra semantic importance."""

    tag = "b"


class Base(Element):
    """Specifies the base URL used for relative URLs in the document."""

    tag = "base"


class Bdi(Element):
    """Isolates text direction from surrounding text."""

    tag = "bdi"


class Bdo(Element):
    """Overrides the current text direction."""

    tag = "bdo"


class Blockquote(Element):
    """Represents a section quoted from another source."""

    tag = "blockquote"


class Body(Element):
    """Contains the visible content of the document."""

    tag = "body"


class Br(Element):
    """Inserts a line break."""

    tag = "br"


class Button(Element):
    """Represents a clickable button control."""

    tag = "button"


class Canvas(Element):
    """Provides a bitmap drawing surface scripted with JavaScript."""

    tag = "canvas"


class Caption(Element):
    """Represents the caption of a table."""

    tag = "caption"


class Cite(Element):
    """Represents the title of a referenced creative work."""

    tag = "cite"


class Code(Element):
    """Represents a fragment of computer code."""

    tag = "code"


class Col(Element):
    """Represents a column within a table column group."""

    tag = "col"


class Colgroup(Element):
    """Groups columns in a table for shared formatting."""

    tag = "colgroup"


class Data(Element):
    """Associates content with a machine-readable value."""

    tag = "data"


class Datalist(Element):
    """Provides predefined options for input controls."""

    tag = "datalist"


class Dd(Element):
    """Represents a description entry in a description list."""

    tag = "dd"


class Del(Element):
    """Represents deleted content."""

    tag = "del"


class Details(Element):
    """Represents a disclosure widget for expandable details."""

    tag = "details"


class Dfn(Element):
    """Represents the defining instance of a term."""

    tag = "dfn"


class Dialog(Element):
    """Represents a dialog box or interactive component."""

    tag = "dialog"


class Div(Element):
    """Represents a generic block container."""

    tag = "div"


class Dl(Element):
    """Represents a description list."""

    tag = "dl"


class Dt(Element):
    """Represents a term in a description list."""

    tag = "dt"


class Em(Element):
    """Represents stress emphasis."""

    tag = "em"


class Embed(Element):
    """Embeds external content at the insertion point."""

    tag = "embed"


class Fieldset(Element):
    """Groups related form controls."""

    tag = "fieldset"


class Figcaption(Element):
    """Represents a caption for figure content."""

    tag = "figcaption"


class Figure(Element):
    """Represents self-contained content with optional caption."""

    tag = "figure"


class Footer(Element):
    """Represents footer content for a page or section."""

    tag = "footer"


class Form(Element):
    """Represents an interactive form."""

    tag = "form"


class H1(Element):
    """Represents a top-level heading."""

    tag = "h1"


class H2(Element):
    """Represents a second-level heading."""

    tag = "h2"


class H3(Element):
    """Represents a third-level heading."""

    tag = "h3"


class H4(Element):
    """Represents a fourth-level heading."""

    tag = "h4"


class H5(Element):
    """Represents a fifth-level heading."""

    tag = "h5"


class H6(Element):
    """Represents a sixth-level heading."""

    tag = "h6"


class Head(Element):
    """Contains metadata for the document."""

    tag = "head"


class Header(Element):
    """Represents introductory content for a page or section."""

    tag = "header"


class Hr(Element):
    """Represents a thematic break between paragraphs."""

    tag = "hr"


class Html(Element):
    """Represents the root element of an HTML document."""

    tag = "html"


class I(Element):  # noqa: E742
    """Represents text in an alternate voice or mood."""

    tag = "i"


class Iframe(Element):
    """Embeds another HTML document."""

    tag = "iframe"


class Img(Element):
    """Embeds an image."""

    tag = "img"


class Input(Element):
    """Represents an input control."""

    tag = "input"


class Ins(Element):
    """Represents inserted content."""

    tag = "ins"


class Kbd(Element):
    """Represents user input from a keyboard or similar device."""

    tag = "kbd"


class Label(Element):
    """Represents a caption for a form control."""

    tag = "label"


class Legend(Element):
    """Represents a caption for a fieldset."""

    tag = "legend"


class Li(Element):
    """Represents a list item."""

    tag = "li"


class Link(Element):
    """Links an external resource, such as a stylesheet."""

    tag = "link"


class Main(Element):
    """Represents the dominant content of the document body."""

    tag = "main"


class Map(Element):
    """Defines an image map with clickable regions."""

    tag = "map"


class Mark(Element):
    """Represents highlighted text for reference."""

    tag = "mark"


class Menu(Element):
    """Represents a list of commands or options."""

    tag = "menu"


class Meta(Element):
    """Represents metadata not covered by other head elements."""

    tag = "meta"


class Meter(Element):
    """Represents a scalar measurement within a known range."""

    tag = "meter"


class Nav(Element):
    """Represents a section containing navigation links."""

    tag = "nav"


class Noscript(Element):
    """Represents fallback content when scripts are unavailable."""

    tag = "noscript"


class Object(Element):
    """Represents an external resource, such as media."""

    tag = "object"


class Ol(Element):
    """Represents an ordered list."""

    tag = "ol"


class Optgroup(Element):
    """Groups related options in a select control."""

    tag = "optgroup"


class Option(Element):
    """Represents a selectable option in a form control."""

    tag = "option"


class Output(Element):
    """Represents the result of a calculation or user action."""

    tag = "output"


class P(Element):
    """Represents a paragraph."""

    tag = "p"


class Param(Element):
    """Defines parameters for an object element."""

    tag = "param"


class Picture(Element):
    """Provides multiple image resources for responsive rendering."""

    tag = "picture"


class Pre(Element):
    """Represents preformatted text."""

    tag = "pre"


class Progress(Element):
    """Represents progress completion for a task."""

    tag = "progress"


class Q(Element):
    """Represents a short inline quotation."""

    tag = "q"


class Rp(Element):
    """Provides fallback parentheses for ruby annotations."""

    tag = "rp"


class Rt(Element):
    """Represents ruby annotation text."""

    tag = "rt"


class Ruby(Element):
    """Represents ruby annotations for East Asian typography."""

    tag = "ruby"


class S(Element):
    """Represents content that is no longer accurate or relevant."""

    tag = "s"


class Samp(Element):
    """Represents sample output from a program."""

    tag = "samp"


class Script(Element):
    """Embeds executable script content."""

    tag = "script"


class Section(Element):
    """Represents a standalone section of content."""

    tag = "section"


class Select(Element):
    """Represents a select control."""

    tag = "select"


class Slot(Element):
    """Defines an insertion point in a web component template."""

    tag = "slot"


class Small(Element):
    """Represents side comments or small print."""

    tag = "small"


class Source(Element):
    """Specifies media resources for media or picture elements."""

    tag = "source"


class Span(Element):
    """Represents a generic inline container."""

    tag = "span"


class Strong(Element):
    """Represents strong importance."""

    tag = "strong"


class Style(Element):
    """Embeds CSS style rules."""

    tag = "style"


class Sub(Element):
    """Represents subscript text."""

    tag = "sub"


class Summary(Element):
    """Represents a summary for a details element."""

    tag = "summary"


class Sup(Element):
    """Represents superscript text."""

    tag = "sup"


class Svg(Element):
    """Represents an SVG drawing container."""

    tag = "svg"


class Table(Element):
    """Represents tabular data."""

    tag = "table"


class Tbody(Element):
    """Groups body rows in a table."""

    tag = "tbody"


class Td(Element):
    """Represents a data cell in a table."""

    tag = "td"


class Template(Element):
    """Holds markup fragments that are not rendered immediately."""

    tag = "template"


class Textarea(Element):
    """Represents a multi-line plain-text editing control."""

    tag = "textarea"


class Tfoot(Element):
    """Groups footer rows in a table."""

    tag = "tfoot"


class Th(Element):
    """Represents a header cell in a table."""

    tag = "th"


class Thead(Element):
    """Groups header rows in a table."""

    tag = "thead"


class Time(Element):
    """Represents a specific date or time."""

    tag = "time"


class Title(Element):
    """Represents the document title."""

    tag = "title"


class Tr(Element):
    """Represents a row in a table."""

    tag = "tr"


class Track(Element):
    """Specifies timed text tracks for media elements."""

    tag = "track"


class U(Element):
    """Represents non-textual annotation styling."""

    tag = "u"


class Ul(Element):
    """Represents an unordered list."""

    tag = "ul"


class Var(Element):
    """Represents a variable in code or math expressions."""

    tag = "var"


class Video(Element):
    """Embeds video content."""

    tag = "video"


class Wbr(Element):
    """Represents a line-break opportunity."""

    tag = "wbr"
