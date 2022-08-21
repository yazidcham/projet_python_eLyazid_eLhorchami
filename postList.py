from .menu import MenuGenerator
from .post import Post

class PostList:
    def __init__(self) -> None:
        pass

    def show(self, listOfPosts: list[Post]):
        if len(listOfPosts) == 0:
            print("Le mur est vide ! Vos amis n'ont rien partagé jusqu'à maintenant")
            return

        menu = MenuGenerator("--- Choisir l'une des options suivantes pour l'ordre d'affichage:", [
            "Affichage du plus récent au plus ancien",
            "Affichage du plus ancien au plus récent"
        ])

        match menu.getChoice():
            case 1:
                self.__showNewToOld(listOfPosts)
            case 2:
                self.__showOldToNew(listOfPosts)

    def __showOldToNew(self, listOfPosts: list[Post]):
        listOfPosts.sort(key=lambda x: x.postDate)
        self.__showList(listOfPosts)

    def __showNewToOld(self, listOfPosts: list[Post]):
        listOfPosts.sort(key=lambda x: x.postDate, reverse=True)
        self.__showList(listOfPosts)

    def __showList(self, listOfPosts: list[Post]):
        print(f"------ Le mur contient {len(listOfPosts)} posts actuellement -----\n")
        for post in listOfPosts:
            print("#" * 30)
            print(f"### Nom d'utilisateur: {post.username}")
            print(f"### Date du poste: {post.postDate}")
            print(f"### Contenu: {post.content}")
            print("#" * 30)
            print("")
            