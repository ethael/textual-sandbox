from textual.app import App, ComposeResult
from textual.widgets import Static, Footer, Label, ListItem, ListView, Markdown
from textual import events
from textual.message import Message


class ArticleList(Static):
    DEFAULT_CSS = """
        ArticleList {
            height: 50%;
            width: 100%;
        }
        ArticleList ListView {
            padding: 0;
            background: black;
            border: solid white;
            scrollbar-size: 1 1;
            height: 100%;
        }
        ArticleList ListItem {
            background: black;
            color: white;
        }
    """

    class Moved(Message):
        def __init__(self, index: int) -> None:
            self.index = index
            super().__init__()


    def compose(self) -> ComposeResult:
        yield ListView(
            ListItem(Label("One")),
            ListItem(Label("Two")),
            ListItem(Label("Three")),
            ListItem(Label("Four")),
            ListItem(Label("Five")),
            ListItem(Label("Six")),
            ListItem(Label("Seven")),
            ListItem(Label("Eight")),
            ListItem(Label("Nine")),
            ListItem(Label("Ten")),
            ListItem(Label("Eleven")),
        )
        yield Footer()

    def index(self) -> None:
        list_view = self.query_one(ListView)
        return list_view.index


    def focus(self) -> None:
        list_view = self.query_one(ListView)
        list_view.focus()


    def on_key(self, event: events.Key) -> None:
        if event.key == "g":
            list_view = self.query_one(ListView)
            list_view.index = 0
            self.post_message(self.Moved(list_view.index)) 
        if event.key == "G":
            list_view = self.query_one(ListView)
            list_view.index = self.list_size - 1
            self.post_message(self.Moved(list_view.index)) 
        if event.key == "j":
            list_view = self.query_one(ListView)
            list_view.index = list_view.index + 1
            self.post_message(self.Moved(list_view.index)) 
        if event.key == "k":
            list_view = self.query_one(ListView)
            list_view.index = list_view.index - 1
            self.post_message(self.Moved(list_view.index)) 


class ArticleDetail(Static):

    DEFAULT_CSS = """
        ArticleDetail {
            height: 50%;
            width: 100%;
        }
        ArticleDetail Markdown {
            background: black;
            border: solid white;
            color: $text;
            scrollbar-size: 1 1;
            overflow-y: auto;
            overflow-x: hidden;
            width: 100%;
            height: 100%;
            margin:  0 1;
        }
    """

    def compose(self) -> ComposeResult:
        yield Markdown("")

    def reset(self, article_body):
        content = self.query_one(Markdown)
        content.update(article_body)
        content.scroll_home()

    def focus(self) -> None:
        content = self.query_one(Markdown)
        content.focus()

    def on_key(self, event: events.Key) -> None:
        content = self.query_one(Markdown)
        if event.key == "g":
            content.scroll_home()
        if event.key == "G":
            content.scroll_end()
        if event.key == "j":
            content.scroll_down()
        if event.key == "k":
            content.scroll_up()

class Poc(App):

    def compose(self) -> ComposeResult:
        yield ArticleList()
        yield ArticleDetail()

    async def on_key(self, event: events.Key) -> None:
        if event.key == "q":
            exit() 
        if event.key == "d":
            article_detail = self.query_one(ArticleDetail)
            article_detail.focus()
        if event.key == "l":
            article_list = self.query_one(ArticleList)
            article_list.focus()

    def update_right_panel(self) -> None:
        article_list = self.query_one(ArticleList)
        article_detail = self.query_one(ArticleDetail)
        article_detail.reset(f"ITEM: {article_list.index()}")

    def on_article_list_moved(self, message: ArticleList.Moved) -> None:
        self.update_right_panel()


if __name__ == "__main__":
    app = Poc()
    app.run()
