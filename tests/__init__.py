
from application import Application, VALID_BLOCK, VALID_CELL, BLOCK, CELL

def statusbar_text(app, index=None):
    if index is None:
        return list(map(lambda x: x.cget('text'), app.statusbar.labels))
    return app.statusbar.labels[index].cget('text')

def select_cell(app, color, cell):
    """
    select colored stone on block and cell location

    Assert:
        Home_block: stone_cell has stone
        Attack_block: stone_cell has stone

    Click Home stone
    Click Destination stone
    Click Attack stone

    Verify:
        Original Attack_block/stone_cell is highlighted

    :param app: pushing stones app
    :param color: black, white, empty
    :param cell: column, row
    :return: true (verified), false(problem) - may return empty for true and description for error
    """
    app_cell = find_cell(app, cell)
    if app_cell is None:
        return 'Cell not found. may be invalid column and row in block or cell'
    if app_cell.cget('text') != color:
        return f'Cell not expected color: expected: {color}, actual: {app_cell.cget("text")}'
    app_cell.button.invoke()
    error = ''

    return error

def verify_cell_details(app, style, color, cell):
    """
    verify block, cell is in state.
    verify block, cell has color

    :param app: pushing stones app
    :param style: cell style used for highlighted or normal
    :param color: black, white, empty
    :param cell: column, row
    :return: true (verified), false(problem) - may return empty for true and description for error
    """
    error = ''
    found_cell = find_cell(app, cell)
    if found_cell is None:
        return 'Cell not found. may be invalid column and row in block or cell'
    # verify state: raised or normal
    if found_cell['style'] != style:
        return f'Cell invalid style: expected {style}, actual: {found_cell["style"]}'
    if found_cell.cget('text') != color:
        return f'Cell not expected color: expected: {color}, actual: {found_cell.cget("text")}'

    return error

def find_cell(app, cell):
    """
    find cell in block on board in app

    :param app: pushing stones app
    :param cell: block, (0-3), (0-3)
    :return: null if no cell found (bad block values, bad cell values
    """
    if VALID_BLOCK(cell.block) and VALID_CELL(cell):
        app_block = app.board_frame.blocks[cell.block.column][cell.block.row]
        app_cell = app_block.cells[cell.column][cell.row]
        return app_cell
    else:
        return None

def verify_cells(app, color, stones_list, captured=None):
    """

    :param app:
    :param color:
    :param stones_list:
    :param captured:
    :return:
    """
    errors = []
    for block, stones in stones_list.items():
        (block_column, block_row) = block.split(',')
        block_column = int(block_column)
        block_row = int(block_row)
        for stone in stones:
            if stone is None:
                continue  # consider checking captured stones todo: finish developing captured stones
            actual_cell = app.board_frame.blocks[block_column][block_row].cells[stone.row][stone.column].cget('text')
            if actual_cell != color:
                errors.append(
                    f'expected stone not at block({block_column}, {block_row}, cell({stone}. expected {color}, actual {actual_cell}')

    # verify captured stones
    return errors

def cell_status(cell):
    # f'block {block_loc.column} {block_loc.row} {dest_cell.column} {dest_cell.row}',
    return f'block {cell.block.column} {cell.block.row} {cell.column} {cell.row}'

def find_stones_on_blocks(app, color, block=None):
    if block is None:
        stones_on_board = []
        for column in range(2):
            stones_on_block = []
            for row in range(2):
                stones_on_block.append(find_stones(app, color, BLOCK(column, row)))
            stones_on_board.append(stones_on_block)
        return stones_on_board
    else:
        return find_stones(app, color, block)

def find_stones(app, color, block):
    stones_in_block = []
    for column in range(4):
        for row in range(4):
            cell = app.board_frame.blocks[block.column][block.row].cells[column][row]
            if cell.cget('text') == color:
                stones_in_block.append(cell)
    return stones_in_block
