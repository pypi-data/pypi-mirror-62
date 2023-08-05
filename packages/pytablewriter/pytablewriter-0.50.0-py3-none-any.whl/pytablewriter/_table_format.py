"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import enum
from typing import Any, List

from .writer import (
    CsvTableWriter,
    ElasticsearchWriter,
    ExcelXlsTableWriter,
    ExcelXlsxTableWriter,
    HtmlTableWriter,
    JavaScriptTableWriter,
    JsonLinesTableWriter,
    JsonTableWriter,
    LatexMatrixWriter,
    LatexTableWriter,
    LtsvTableWriter,
    MarkdownTableWriter,
    MediaWikiTableWriter,
    NullTableWriter,
    NumpyTableWriter,
    PandasDataFrameWriter,
    PythonCodeTableWriter,
    RstCsvTableWriter,
    RstGridTableWriter,
    RstSimpleTableWriter,
    SpaceAlignedTableWriter,
    SqliteTableWriter,
    TomlTableWriter,
    TsvTableWriter,
    UnicodeTableWriter,
)


class FormatAttr:
    """
    Bitmaps to represent table attributes.
    """

    NONE = 1 << 1

    #: Can create a file with the format.
    FILE = 1 << 2

    #: Table format that can represent as a text.
    TEXT = 1 << 3

    #: Table format that can represent as a binary file.
    BIN = 1 << 4

    #: Can create a source code (variables definition)
    #: one of the programming language.
    SOURCECODE = 1 << 5

    #: Can call API for external service.
    API = 1 << 6

    SECONDARY_EXT = 1 << 10
    SECONDARY_NAME = 1 << 11


@enum.unique
class TableFormat(enum.Enum):
    """
    Enum to represent table format attributes.
    """

    CSV = ([CsvTableWriter.FORMAT_NAME], CsvTableWriter, FormatAttr.FILE | FormatAttr.TEXT, ["csv"])
    ELASTICSEARCH = (
        [ElasticsearchWriter.FORMAT_NAME],  # type: ignore
        ElasticsearchWriter,
        FormatAttr.API,
        [],
    )
    EXCEL_XLS = (
        [ExcelXlsTableWriter.FORMAT_NAME],
        ExcelXlsTableWriter,
        FormatAttr.FILE | FormatAttr.BIN | FormatAttr.SECONDARY_NAME,
        ["xls"],
    )
    EXCEL_XLSX = (
        [ExcelXlsxTableWriter.FORMAT_NAME],
        ExcelXlsxTableWriter,
        FormatAttr.FILE | FormatAttr.BIN,
        ["xlsx"],
    )
    HTML = (
        [HtmlTableWriter.FORMAT_NAME, "htm"],
        HtmlTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT,
        ["html", "htm"],
    )
    JAVASCRIPT = (
        [JavaScriptTableWriter.FORMAT_NAME, "js"],
        JavaScriptTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SOURCECODE,
        ["js"],
    )
    JSON = (
        [JsonTableWriter.FORMAT_NAME],
        JsonTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT,
        ["json"],
    )
    JSON_LINES = (
        [JsonLinesTableWriter.FORMAT_NAME, "jsonl", "ldjson", "ndjson"],
        JsonLinesTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT,
        ["jsonl", "ldjson", "ndjson"],
    )
    LATEX_MATRIX = (
        [LatexMatrixWriter.FORMAT_NAME],
        LatexMatrixWriter,
        FormatAttr.FILE | FormatAttr.TEXT,
        ["tex"],
    )
    LATEX_TABLE = (
        [LatexTableWriter.FORMAT_NAME],
        LatexTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SECONDARY_EXT,
        ["tex"],
    )
    LTSV = (
        [LtsvTableWriter.FORMAT_NAME],
        LtsvTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT,
        ["ltsv"],
    )
    MARKDOWN = (
        [MarkdownTableWriter.FORMAT_NAME, "md"],
        MarkdownTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT,
        ["md"],
    )
    MEDIAWIKI = (
        [MediaWikiTableWriter.FORMAT_NAME],  # type: ignore
        MediaWikiTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT,
        [],
    )
    NULL = (
        [NullTableWriter.FORMAT_NAME],  # type: ignore
        NullTableWriter,
        FormatAttr.NONE,
        [],
    )
    NUMPY = (
        [NumpyTableWriter.FORMAT_NAME],
        NumpyTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SOURCECODE | FormatAttr.SECONDARY_EXT,
        ["py"],
    )
    PANDAS = (
        [PandasDataFrameWriter.FORMAT_NAME],
        PandasDataFrameWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SOURCECODE | FormatAttr.SECONDARY_EXT,
        ["py"],
    )
    PYTHON = (
        [PythonCodeTableWriter.FORMAT_NAME, "py"],
        PythonCodeTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SOURCECODE,
        ["py"],
    )
    RST_CSV_TABLE = (
        [RstCsvTableWriter.FORMAT_NAME, "rst_csv"],
        RstCsvTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SECONDARY_EXT,
        ["rst"],
    )
    RST_GRID_TABLE = (
        [RstGridTableWriter.FORMAT_NAME, "rst_grid", "rst"],
        RstGridTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT,
        ["rst"],
    )
    RST_SIMPLE_TABLE = (
        [RstSimpleTableWriter.FORMAT_NAME, "rst_simple"],
        RstSimpleTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SECONDARY_EXT,
        ["rst"],
    )
    SPACE_ALIGNED = (
        [SpaceAlignedTableWriter.FORMAT_NAME],  # type: ignore
        SpaceAlignedTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT,
        [],
    )
    SQLITE = (
        [SqliteTableWriter.FORMAT_NAME],
        SqliteTableWriter,
        FormatAttr.FILE | FormatAttr.BIN,
        ["sqlite", "sqlite3"],
    )
    TOML = (
        [TomlTableWriter.FORMAT_NAME],
        TomlTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT,
        ["toml"],
    )
    TSV = ([TsvTableWriter.FORMAT_NAME], TsvTableWriter, FormatAttr.FILE | FormatAttr.TEXT, ["tsv"])
    UNICODE = (
        [UnicodeTableWriter.FORMAT_NAME],  # type: ignore
        UnicodeTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT,
        [],
    )

    @property
    def names(self) -> List[str]:
        """
        :return: Names associated with the table format.
        :rtype: list
        """

        return self.__names

    @property
    def writer_class(self) -> Any:
        """
        :return: Table writer class associated with the table format.
        :rtype:
            :py:class:`~pytablewriter.writer._table_writer.TableWriterInterface`
        """

        return self.__writer_class

    @property
    def format_attribute(self) -> int:
        """
        :return: Table attributes bitmap.
        :rtype: :py:class:`pytablewriter.FormatAttr`
        """

        return self.__format_attribute

    @property
    def file_extensions(self) -> List[str]:
        """
        :return: File extensions associated with the table format.
        :rtype: list
        """

        return self.__file_extensions

    def __init__(self, names, writer_class, format_attribute, file_extensions):
        self.__names = names
        self.__writer_class = writer_class
        self.__format_attribute = format_attribute
        self.__file_extensions = file_extensions

    @classmethod
    def find_all_attr(cls, format_attribute: int) -> List:
        """
        Searching table formats which have specific attributes.

        :param FormatAttr format_attribute:
            Table format attributes to look for.
        :return: Table formats that matched the attribute.
        :rtype: list
        """

        return [
            table_format
            for table_format in TableFormat
            if table_format.format_attribute & format_attribute
        ]
