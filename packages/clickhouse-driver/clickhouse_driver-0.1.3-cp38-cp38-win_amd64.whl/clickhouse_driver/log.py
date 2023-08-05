import logging

logger = logging.getLogger(__name__)


log_priorities = (
    'Unknown',
    'Fatal',
    'Critical',
    'Error',
    'Warning',
    'Notice',
    'Information',
    'Debug',
    'Trace'
)


def log_block(block):
    column_names = [x[0] for x in block.columns_with_types]

    for row in block.get_rows():
        row = dict(zip(column_names, row))

        if 1 <= row['priority'] <= 8:
            priority = log_priorities[row['priority']]
        else:
            priority = row[0]

        logger.info(
            '{%s} [ %s ] <%s> %s: %s',
            row['query_id'],
            row['thread_number'],
            priority,
            row['source'],
            row['text']
        )
