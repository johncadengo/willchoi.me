import time, threading

from flask.ext.script import Manager

from instagram.client import InstagramAPI

from app import app, db
from app.models import Image, Location, Photo, Tag

manager = Manager(usage='Perform database operations')


def get_media(feed):
    g = (media for medias, next in feed for media in medias)
    while g:
        try:
            yield g.next()
        except AttributeError:
            break


@manager.command
def create(access_token=None):
    'Create db tables'
    db.create_all()
    if access_token:
        populate(access_token)


@manager.command
def populate(access_token):
    'Populate database with default data'
    user_id = app.config.get('INSTAGRAM_USER_ID')

    api = InstagramAPI(access_token=access_token)
    feed = api.user_recent_media(user_id=user_id, max_pages=2000, as_generator=True)

    all_tags = {}
    for media in get_media(feed):
        # Add photos
        caption = media.caption.text if media.caption else None
        photo = Photo(
            instagram_id=media.id,
            caption=caption,
            created_time=media.created_time,
            link=media.link)
        db.session.add(photo)

        # Add tags, ensure we do not duplicate tags
        if hasattr(media, 'tags'):
            tags = {t.name: all_tags.get(t.name, Tag(name=t.name)) for t in media.tags}
            all_tags.update(tags)
            photo.tags.extend(tags.values())

        # Add images
        images = [Image(height=i.height, width=i.width, url=i.url, type=i_type)
                  for i_type, i in media.images.iteritems()]
        db.session.add_all(images)
        photo.images.extend(images)

        # TODO: Locations.

    db.session.add_all(all_tags.values())
    db.session.commit()

