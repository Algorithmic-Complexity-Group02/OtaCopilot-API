class UserProfile:
    def __init__(self, profile, gender, birthday, favorites_anime, link):
        self.profile = profile
        self.gender = gender
        self.birthday = birthday
        self.favorites_anime = favorites_anime
        self.link = link 
    
    
    def __str__(self):
        return f'UserProfile(profile={self.profile}, gender={self.gender}, birthday={self.birthday}, favorites_anime={self.favorites_anime}, link={self.link})'