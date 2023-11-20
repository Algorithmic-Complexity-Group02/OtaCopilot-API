class Anime:

    def __init__(self, uid, title, genre, aired, episodes, members, popularity, ranked, score, img_url, link):
        self.uid = uid
        self.title = title
        self.genre = genre
        self.aired = aired
        self.episodes = episodes
        self.members = members
        self.popularity = popularity
        self.ranked = ranked
        self.score = score
        self.img_url = img_url
        self.link = link
    
    def __str__(self):
        return f'Anime(uid={self.uid}, title={self.title}, genre={self.genre}, episodes={self.episodes}, popularity={self.popularity}, ranked={self.ranked}, score={self.score}, img_url={self.img_url}, link={self.link})'