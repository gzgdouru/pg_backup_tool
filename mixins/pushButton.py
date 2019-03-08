from PyQt5.QtWidgets import QPushButton


class CommitPushButtonMixin(object):
    '''创建commit PushButton部件'''

    def create_commit_PushButton(self, *args, **kwargs):
        label = kwargs.get("commit_label", "提交")
        bt = QPushButton(label)
        bt.clicked.connect(self.commit)
        self.add_widget(bt, 0)

        return bt


class CancelPushButtonMixin(object):
    '''创建cancel PushButton部件'''

    def create_cancel_PushButton(self, *args, **kwargs):
        label = kwargs.get("cancel_label", "取消")
        bt = QPushButton(label)
        bt.clicked.connect(self.cancel)
        self.add_widget(bt, 1)

        return bt
