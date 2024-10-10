from math import ceil
from flask import request

def paginate(query, page=1, per_page=10):
    """
    Paginate a query and return the paginated results.

    :param query: The query to paginate.
    :param page: The page number to retrieve (default: 1).
    :param per_page: The number of items per page (default: 10).
    """
    # Get the total number of items
    total_items = query.count()

    # Calculate the number of pages
    total_pages = ceil(total_items / per_page)

    # Calculate the start and end indices
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    # Paginate the query
    items = query.limit(per_page).offset(start_index).all()

    # Return the paginated results
    return {
        'items': items,
        'total_items': total_items,
        'total_pages': total_pages,
        'current_page': page,
        'per_page': per_page,
        'next_page': page + 1 if page < total_pages else None,
        'prev_page': page - 1 if page > 1 else None,
    }

def get_page_args():
    """
    Get the pagination arguments from the request.

    :return: A tuple containing the page number and per-page count.
    """
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    return page, per_page
