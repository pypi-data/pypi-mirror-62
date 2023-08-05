from contextlib import contextmanager

from django.conf import settings
from django.utils import timezone

from isc_common.auth.models.user import User
from isc_common.bit import IsBitOff
from isc_common.models.progresses import Progresses
from isc_common.ws.progressStack import ProgressStack


class ProgressDroped(Exception):
    ...


@contextmanager
def managed_progress(qty, user, id, message='Обработано позиций', title='Обработано позиций', props=0):
    progress = Progress(id=id, qty=qty, user=user, message=message, title=title, props=props)
    try:
        yield progress
        progress.close()
    except Exception as ex:
        progress.close()
        if callable(progress.except_func):
            progress.except_func(progress)
        raise ex


def clean_progresses():
    Progresses.objects.all().delete()


class Progress:
    progress = None
    except_func = None

    def __init__(self, qty, user, id, message='Обработано позиций', title='Обработано позиций', props=0):
        self.message = message
        self.title = title
        self.props = props
        self.id = id

        if isinstance(user, int):
            self.user = User.objects.get(id=user)
        elif not isinstance(user, User):
            raise Exception(f'user must be User instance.')
        else:
            self.user = user
        self.qty = qty

        if self.qty > 0:
            channel = f'common_{self.user.username}'
            self.progress = ProgressStack(
                host=settings.WS_HOST,
                port=settings.WS_PORT,
                channel=channel,
                props=self.props,
                user_id=self.user.id
            )

            self.demand_str = f'<h3>{self.message}</h3>'

            if not self.check_exists():
                self.progress.show(
                    cntAll=qty,
                    id=self.id,
                    label_contents=self.demand_str,
                    title=f'<b>{title}</b>',
                )

                if IsBitOff(props, 1):
                    self.progresses, created = Progresses.objects.get_or_create(
                        id_progress=self.id,
                        user=self.user,
                        defaults=dict(
                            cnt=0,
                            label_contents=self.demand_str,
                            qty=self.qty,
                            message=self.message,
                            props=self.props,
                            title=self.title,
                            lastmodified=timezone.now()
                        )
                    )

        self.cnt = 0

    def check_4_exit(self):
        from isc_common.models.deleted_progresses import Deleted_progresses
        res = 0
        for delted_process in Deleted_progresses.objects.filter(id_progress=self.id, user=self.user):
            res += 1
            delted_process.delete()

        return res

    def check_exists(self):
        res = Progresses.objects.filter(
            id_progress=self.id,
            user=self.user
        ).count() > 0

    def step(self):
        res = 0
        if self.progress != None:
            self.progress.setCntDone(self.cnt, self.id)
            self.cnt += 1
            if self.qty == self.cnt:
                self.cnt = 0
            self.progresses.cnt = self.cnt
            self.progresses.lastmodified = timezone.now()
            self.progresses.save()
            res = self.check_4_exit()
            return res

    def setContentsLabel(self, content):
        if self.progress != None:
            self.progress.setContentsLabel(labelContents=content, id=self.id)
            self.progresses.labelContents = content
            self.progresses.save()

    def sendInfo(self, message):
        if self.progress != None:
            self.progress.sendInfo(message=message)

    def sendWarn(self, message):
        if self.progress != None:
            self.progress.sendWarn(message=message)

    def sendMessage(self, type, message=None):
        if self.progress != None:
            self.progress.sendMessage(type=type, message=message)

    def close(self):
        if self.progress != None:
            self.progress.close(self.id)
            try:
                self.progresses.delete()
            except AssertionError:
                pass
