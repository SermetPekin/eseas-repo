def view_display(*msg):
    from rich.console import Console
    from rich.panel import Panel

    console = Console()
    for item in msg:
        item = str(item)
        # Use a simple dark background with standard text
        panel = Panel(item.strip(), style="on #1e1e1e", expand=False)
        console.print(panel)

test_str = """========================================================================
        common_space_check has run
test : False
folder to check demetra files : eseas/data_for_testing/unix
========================================================================"""
view_display(test_str)
