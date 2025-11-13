import re
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from difflib import get_close_matches

class QueryClassifier:
    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.model = MultinomialNB()
        self.train_model()

    def train_model(self):
        X_train = [
            "who is elon musk", "who is bill gates", "who is jeff bezos", "who is mark zuckerberg",
            "who is sundar pichai", "who is satya nadella", "who is tim cook", "who is donald trump",
            "who is joe biden", "who is narendra modi", "who is rahul gandhi", "who is virat kohli",
            "who is ms dhoni", "who is sachin tendulkar", "who is rohit sharma", "who is cristiano ronaldo",
            "who is lionel messi", "who is taylor swift", "who is selena gomez", "who is ariana grande",
            "who is shah rukh khan", "who is salman khan", "who is amitabh bachchan", "who is priyanka chopra",
            "what is the weather today", "current temperature in delhi", "weather in mumbai",
            "weather forecast bangalore", "temperature in kolkata", "will it rain today",
            "weather report chennai", "climate in hyderabad", "weather in pune today",
            "temperature right now", "is it going to rain", "weather forecast for tomorrow",
            "weather in new york", "temperature in london", "weather in dubai",
            "today match score", "live cricket score", "match between india and england",
            "india vs pakistan match update", "today's cricket score", "live football match update",
            "ipl score today", "who won today's match", "cricket match live", "football score now",
            "match result india vs australia", "world cup final score", "premier league results",
            "nba game score", "tennis match live", "olympics medal tally",
            "latest news headlines", "breaking news india", "top news", "what happened today",
            "latest updates today", "what is trending now", "news today", "current affairs",
            "breaking news world", "political news india", "sports news today", "tech news",
            "bollywood news latest", "entertainment news", "business news india", "economy updates",
            "how many subscribers does sourav joshi have", "followers of virat kohli",
            "youtube subscribers count", "instagram followers of ronaldo", "twitter followers of elon musk",
            "pewdiepie subscriber count", "mr beast subscribers", "subscribers of carryminati",
            "followers of selena gomez", "how many followers does kylie jenner have",
            "net worth of ms dhoni", "stock price of apple", "tesla stock price",
            "bitcoin price today", "gold rate today", "silver price now", "reliance stock price",
            "tcs share price", "infosys stock", "dollar rate today", "rupee to dollar conversion",
            "crypto prices today", "ethereum price now", "dogecoin value",
            "what is the population of india", "population of china", "how many people in usa",
            "population of mumbai", "delhi population", "world population now",
            "ceo of google", "ceo of microsoft", "who owns tesla", "founder of facebook",
            "ceo of apple", "who is the ceo of amazon", "owner of spacex", "ceo of nvidia",
            "founder of openai", "who runs twitter", "ceo of meta", "owner of youtube",
            "hello", "hi", "hey", "good morning", "good evening", "good night", "good afternoon",
            "what's up", "wassup", "yo", "sup", "greetings", "namaste", "hey there", "hi there",
            "who are you", "what is your name", "tell me about yourself", "who made you",
            "who created you", "who trained you", "who is your creator", "what can you do",
            "what are your capabilities", "how do you work", "are you human", "are you ai",
            "what is your purpose", "why were you created", "who developed you",
            "i am sad", "i feel depressed", "i lost hope in life", "i feel anxious",
            "i'm not okay", "i need help", "i want to die", "i feel lonely", "i am stressed",
            "i feel tired", "i need motivation", "motivate me", "inspire me", "i give up",
            "life is hard", "i can't do this", "i feel worthless", "i hate myself",
            "i am scared", "i have anxiety", "i feel empty", "i need someone to talk",
            "i feel hopeless", "everything is going wrong", "i want to quit",
            "i am happy today", "i feel great", "i am excited", "i feel amazing",
            "i am proud of myself", "i did it", "i feel confident", "i am grateful",
            "tell me a joke", "make me laugh", "say something funny", "tell me a story",
            "sing me a song", "tell me a riddle", "give me a fun fact", "entertain me",
            "i feel bored", "i am bored", "what should i do", "suggest something fun",
            "how are you", "how are you doing", "are you okay", "what's going on",
            "how is your day", "are you fine", "how do you feel",
            "i want to work", "bro i have work", "i want to focus", "give me music to concentrate",
            "i need to study", "help me focus", "i have exam tomorrow", "i need concentration",
            "productivity tips", "how to stay focused", "i am distracted",
            "what is the time now", "current time", "tell me the time", "what time is it",
            "what is current time", "date today", "what's the current time", "what's the date",
            "today's date", "todays date", "what is today date", "what day is it",
            "what month is it", "what year is it",
            "do you sleep", "do you eat", "do you have friends", "are you real",
            "can you think", "do you dream", "what do you like", "what is your favorite color",
            "do you love me", "are you intelligent", "can you feel emotions",
            "okay", "cool", "nice", "awesome", "great", "thanks", "thank you",
            "that's helpful", "i understand", "got it", "makes sense", "interesting",
            "tell me more", "go on", "continue", "what else", "anything else",
            "generate image of a cat", "create image of a dog", "draw a dragon", "make image of mountain",
            "generate ai art of robot", "create cartoon of superman", "make poster of independence day",
            "draw haunted house", "generate anime character", "create digital art of spaceship",
            "conjure artistic depiction of peace", "generate wallpaper of forest", "create mental clarity artwork",
            "draw a unicorn", "generate sunset painting", "create galaxy artwork", "make fantasy landscape",
            "draw futuristic city", "generate cyberpunk art", "create steampunk robot", "make abstract art",
            "draw realistic portrait", "generate sci-fi scene", "create nature wallpaper", "make anime girl",
            "draw superhero poster", "generate horror scene", "create watercolor painting", "make pixel art",
            "draw medieval castle", "generate space station", "create underwater scene", "make neon cityscape",
            "draw cute animals", "generate warrior character", "create mystical forest", "make logo design",
            "draw tribal art", "generate festival poster", "create movie poster", "make book cover design",
            "generate image of iron man", "create picture of taj mahal", "draw image of krishna",
            "make artwork of shiva", "generate image of ganesh", "create picture of ram",
            "write application to principal", "write leave application", "write sick leave application",
            "compose mail to boss", "write letter to friend", "write formal letter", "write complaint letter",
            "write resignation letter", "write cover letter", "write recommendation letter",
            "draft email for sick leave", "write permission letter", "write apology letter",
            "write invitation letter", "write thank you letter", "write appreciation email",
            "write essay on climate change", "write article on technology", "create blog on artificial intelligence",
            "write essay on education", "write article about health", "create blog post on fitness",
            "write essay on pollution", "write article about space", "create content on machine learning",
            "write essay on democracy", "write article on social media", "write blog on entrepreneurship",
            "write essay about friendship", "write article on mental health", "write blog about travel",
            "write story about friendship", "write a short story", "write horror story",
            "write fantasy story", "write love story", "write adventure story", "create fictional narrative",
            "write sci-fi story", "write mystery story", "write fairy tale",
            "create email for job application", "write business proposal", "draft project report",
            "write meeting minutes", "create presentation content", "write product description",
            "draft press release", "write marketing copy", "create social media post",
            "write website content", "draft terms and conditions", "write privacy policy",
            "generate note on pollution", "write summary of article", "create study notes",
            "write research paper", "draft thesis outline", "write literature review",
            "create case study", "write lab report", "generate notes on history",
            "write poem about love", "create song lyrics", "write script for video",
            "draft speech for event", "write biography", "create resume", "write cv",
            "mute the system", "unmute system", "volume up", "volume down", "increase volume",
            "decrease volume", "lower volume", "reduce volume", "raise volume", "max volume",
            "minimum volume", "set volume to 50", "turn up the volume", "turn down the volume",
            "make it louder", "make it quieter", "silence the system", "full volume",
            "increase brightness", "decrease brightness", "dim brightness", "brighten screen",
            "lower brightness", "raise brightness", "max brightness", "minimum brightness",
            "reduce screen brightness", "make screen brighter", "make screen darker",
            "shutdown my pc", "restart laptop", "put system to sleep", "hibernate computer",
            "turn off pc", "reboot system", "power off laptop", "restart my computer",
            "shut down the system", "sleep mode", "restart now",
            "enable bluetooth", "disable bluetooth", "turn on bluetooth", "turn off bluetooth",
            "turn on airplane mode", "turn off airplane mode", "enable flight mode",
            "turn off wifi", "turn on wifi", "disconnect internet", "connect to wifi",
            "enable wifi", "disable wifi", "toggle airplane mode",
            "lock screen", "unlock screen", "turn off display", "rotate screen",
            "change wallpaper", "take screenshot", "screen capture",
            "open task manager", "close all apps", "minimize all windows", "maximize window",
            "switch window", "close current window", "fullscreen mode", "exit fullscreen",
            "open chrome", "open google chrome", "launch chrome browser", "start chrome",
            "open firefox", "launch firefox browser", "open edge", "open brave browser",
            "open opera", "launch safari", "open internet explorer",
            "open youtube", "launch youtube", "open instagram", "launch instagram",
            "open facebook", "open facebook app", "launch facebook", "open twitter",
            "open whatsap", "open whatsap", "start whatsapp", "launch whatsapp",
            "open telegram", "launch telegram", "open snapchat", "open tiktok",
            "open linkedin", "launch linkedin", "open pinterest", "open reddit",
            "open notion", "launch notion", "open settings", "launch settings",
            "open notepad", "launch notepad", "open word", "open microsoft word",
            "open excel", "launch excel", "open powerpoint", "open outlook",
            "open onenote", "launch onenote", "open teams", "open slack",
            "open zoom", "launch zoom", "open google meet", "open skype",
            "launch canva", "open canva", "open photoshop", "launch photoshop",
            "open illustrator", "open premiere pro", "launch after effects",
            "open figma", "launch figma", "open blender", "open gimp",
            "open visual studio code", "launch vscode", "open vs code", "open pycharm",
            "launch pycharm", "open sublime text", "open atom editor", "launch android studio",
            "open git bash", "open command prompt", "launch terminal", "open powershell",
            "open spotify", "launch spotify", "start spotify", "open vlc",
            "launch vlc player", "open windows media player", "open itunes",
            "open file explorer", "launch file manager", "open downloads folder",
            "open documents", "open my computer", "open this pc",
            "open calculator", "launch calculator", "open calendar", "open clock",
            "open paint", "launch paint", "open maps", "open weather app",
            "open camera", "launch camera app", "open discord", "launch discord",
            "close chrome", "exit chrome", "close google chrome", "quit chrome",
            "close settings", "exit settings", "close whatsapp", "stop whatsapp",
            "terminate whatsapp", "close facebook", "shutdown facebook", "exit facebook",
            "close instagram", "shutdown instagram", "quit instagram", "close youtube",
            "exit youtube", "close browser", "close browser tab", "close current tab",
            "stop the music app", "close spotify", "exit spotify", "quit spotify",
            "close notepad", "exit notepad", "close word", "exit microsoft word",
            "close excel", "quit excel", "close powerpoint", "exit outlook",
            "close zoom", "exit zoom meeting", "close teams", "quit teams",
            "close all apps", "close all windows", "close everything", "exit all programs",
            "terminate app", "kill process", "force close", "stop application",
            "play song on spotify", "play music on spotify", "start spotify playback",
            "play kalachashma on spotify", "play lofi music on spotify", "play lofi beats on spotify",
            "start playing bhajan on spotify", "play bhajan on spotify", "play hindi bhajans on spotify",
            "play my playlist on spotify", "play bollywood hits on spotify", "play bollywood songs on spotify",
            "start playback on spotify", "play romantic songs on spotify", "play love songs on spotify",
            "play workout music on spotify", "play gym music on spotify", "play focus music on spotify",
            "play adiye on spotify", "play top 50 india on spotify", "play trending songs on spotify",
            "play chill music on spotify", "play jazz on spotify", "play classical music on spotify",
            "play rock music on spotify", "play pop songs on spotify", "play edm on spotify",
            "play hip hop on spotify", "play rap music on spotify", "play indie music on spotify",
            "play devotional songs on spotify", "play meditation music on spotify", "play sleep music on spotify",
            "play study music on spotify", "play concentration music on spotify", "play calm music on spotify",
            "play party songs on spotify", "play dance music on spotify", "play punjabi songs on spotify",
            "play tamil songs on spotify", "play telugu songs on spotify", "play malayalam songs on spotify",
            "play marathi songs on spotify", "play bengali songs on spotify", "play english songs on spotify",
            "play old songs on spotify", "play retro music on spotify", "play 90s hits on spotify",
            "play arijit singh on spotify", "play shreya ghoshal on spotify", "play neha kakkar on spotify",
            "play badshah on spotify", "play yo yo honey singh on spotify", "play diljit dosanjh on spotify",
            "listen to music on youtube", "play song on youtube", "play video on youtube",
            "play kalachashma on youtube", "play lofi beats on youtube", "play lofi music on youtube",
            "start playing bhajan on youtube", "play bhajan on youtube", "play ramayan on youtube",
            "play my playlist on youtube", "play bollywood hits on youtube", "play hindi songs on youtube",
            "start playback on youtube", "play romantic songs on youtube", "play love songs on youtube",
            "play workout music on youtube", "play gym videos on youtube", "play exercise videos on youtube",
            "play notyourtype on youtube", "play devotional songs on youtube", "play aarti on youtube",
            "play funny videos on youtube", "play comedy videos on youtube", "play stand up comedy on youtube",
            "play movie clips on youtube", "play trailer on youtube", "play web series on youtube",
            "play tech videos on youtube", "play tutorial on youtube", "play how to videos on youtube",
            "play gaming videos on youtube", "play gameplay on youtube", "play minecraft on youtube",
            "play vlogs on youtube", "play travel videos on youtube", "play food videos on youtube",
            "play cooking videos on youtube", "play recipe on youtube", "play baking videos on youtube",
            "play music video on youtube", "play concert on youtube", "play live performance on youtube",
            "play podcast on youtube", "play audiobook on youtube", "play documentary on youtube",
            "play cartoon on youtube", "play anime on youtube", "play kids videos on youtube",
            "play nursery rhymes on youtube", "play baby songs on youtube", "play lullaby on youtube",
            "play meditation on youtube", "play yoga video on youtube", "play guided meditation on youtube",
            "play sleep sounds on youtube", "play rain sounds on youtube", "play asmr on youtube",
            "play news on youtube", "play sports highlights on youtube", "play cricket match on youtube",
            "play football match on youtube", "play music playlist on youtube", "play trending videos on youtube",
            "play viral videos on youtube", "play movie songs on youtube", "play dance videos on youtube",
            "play fitness videos on youtube", "play motivational videos on youtube", "play educational videos on youtube",
            "search virat kohli on google", "search elon musk on google", "search bill gates on google",
            "search romantic songs on google", "search love songs on google", "search sad songs on google",
            "search yoga video on google", "search exercise videos on google", "search workout routine on google",
            "search cricket highlights on google", "search match highlights on google", "search football on google",
            "search ai news on google", "search tech news on google", "search latest technology on google",
            "search diwali songs on google", "search festival songs on google", "search christmas songs on google",
            "search tesla stock on google", "search apple stock on google", "search bitcoin price on google",
            "search india vs pakistan match on google", "search ipl score on google", "search match result on google",
            "search funny cat videos on google", "search dog videos on google", "search animal videos on google",
            "search calm music on google", "search relaxing music on google", "search peaceful music on google",
            "search gaming videos on google", "search gameplay on google", "search game review on google",
            "search healthy recipes on google", "search food recipes on google", "search cooking recipes on google",
            "search news about elections on google", "search political news on google", "search breaking news on google",
            "search cartoon videos on google", "search anime on google", "search movies on google",
            "search iron man on google", "search avengers on google", "search marvel on google",
            "search ramayan on google", "search mahabharata on google", "search mythology on google",
            "search sleep music on google", "search meditation music on google", "search study music on google",
            "search how to cook biryani on google", "search how to make cake on google", "search recipe for pasta on google",
            "search top programming languages on google", "search python tutorial on google", "search learn coding on google",
            "search top 50 songs india on google", "search trending songs on google", "search viral videos on google",
            "search neuroplasticity techniques on google", "search brain training on google", "search memory improvement on google",
            "search travel destinations on google", "search tourist places on google", "search vacation spots on google",
            "search funny memes on google", "search jokes on google", "search riddles on google",
            "search motivational quotes on google", "search inspirational stories on google", "search success stories on google",
            "search fitness tips on google", "search weight loss tips on google", "search diet plan on google",
            "search online courses on google", "search free courses on google", "search certifications on google",
        ]

        y_train = (
            ["realtime"] * 130 +
            ["general"] * 130 +
            ["generate"] * 50 +
            ["content"] * 60 +
            ["system"] * 60 +
            ["open"] * 80 +
            ["close"] * 40 +
            ["play"] * 128 +
            ["search"] * 80
        )

        X_train.extend([
            "play songs on youtube", "play music videos on youtube", "play concert videos on youtube",
            "play bhajans on youtube", "play mantras on youtube", "play devotional music on youtube",
            "play workout playlist on youtube", "play party music on youtube", "play chill beats on youtube",
            "play instrumental music on youtube"
        ])
        y_train.extend(["play"] * 10)

        self.training_corpus = X_train
        self._keywords = list({w for phrase in X_train for w in phrase.split()})

        if len(X_train) != len(y_train):
            min_len = min(len(X_train), len(y_train))
            X_train = X_train[:min_len]
            y_train = y_train[:min_len]

        X_vectors = self.vectorizer.fit_transform(X_train)
        self.model.fit(X_vectors, y_train)
        print(f"Model trained with {len(X_train)} examples across {len(set(y_train))} categories")

    def normalize_aliases(self, query: str) -> str:
        aliases = {
            "whatsapp": "whatsap",
            "whatsp": "whatsap",
            "start whatsapp": "open whatsap",
            "open app whatsap": "open whatsap",
            "open whatsapp": "open whatsap",
            "vscode": "visual studio code",
            "vs code": "visual studio code",
        }
        for k, v in aliases.items():
            pattern = r'\b' + re.escape(k) + r'\b'
            query = re.sub(pattern, v, query)
        return query

    def correct_typo(self, query: str) -> str:
        words = query.split()
        corrected_words = []
        for word in words:
            match = get_close_matches(word, self._keywords, n=1, cutoff=0.85)
            corrected_words.append(match[0] if match else word)
        corrected_query = ' '.join(corrected_words)

        if corrected_query not in self.training_corpus:
            phrase_match = get_close_matches(corrected_query, self.training_corpus, n=1, cutoff=0.8)
            if phrase_match:
                return phrase_match[0]
        return corrected_query

    def classify_single(self, query: str) -> List[str]:
        query = query.lower().strip()
        query = self.normalize_aliases(query)
        query = re.sub(r"^(hey bro\.ai|can you|could you|would you|also|please|kindly|after that|then)\s+", "", query)
        query = re.sub(r"\s+(please|thanks|thank you)$", "", query)

        if query in ['exit', 'quit', 'bye']:
            return ['exit']

        if query.startswith("write") or query.startswith("create") or query.startswith("draft"):
            return [f"content {query}"]

        general_time_phrases = [
            "what is the time now", "current time", "tell me the time", "what time is it",
            "what is current time", "date today", "what's the current time", "what's the date",
            "today's date", "todays date", "what is today date", "what day is it"
        ]
        if get_close_matches(query, general_time_phrases, n=1, cutoff=0.8):
            return [f"general {query}"]

        try:
            query = self.correct_typo(query)
            vec = self.vectorizer.transform([query])
            if vec.nnz == 0:
                return [f"general {query}"]

            label = self.model.predict(vec)[0]
            cleaned_query = query

            if label == "play":
                if any(w in query for w in [
                    "can you", "could you", "would you", "will you", "should i",
                    "i will", "i want", "rate", "how was", "do you like"
                ]):
                    return [f"general {query}"]

                if "spotify" in query or any(w in query for w in ["focus", "concentrate", "work", "study", "chill", "calm"]):
                    return [f"play.spotify {cleaned_query}"]
                elif "youtube" in query or "yt" in query:
                    return [f"play.youtube {cleaned_query}"]
                return [f"play.youtube {cleaned_query}"]

            if label == "generate":
                return [f"generate {cleaned_query}"]

            if label == "system":
                return [f"system {cleaned_query}"]

            if label == "open":
                return [f"open {cleaned_query}"]

            if label == "close":
                return [f"close {cleaned_query}"]

            if label == "search":
                return [f"search {cleaned_query}"]

            if label == "realtime":
                return [f"realtime {cleaned_query}"]

            if label == "content":
                return [f"content {cleaned_query}"]

            if label == "general":
                if any(w in query for w in ["music", "song", "spotify", "youtube", "tune", "beat", "listen", "hear"]):
                    return [f"play.spotify {query}" if "spotify" in query else f"play.youtube {query}"]
                if any(w in query for w in ["image", "draw", "create", "generate", "art", "cartoon", "depiction", "wallpaper", "conjure", "picture"]):
                    return [f"generate {query}"]
                if any(w in query for w in ["search", "google", "find", "look up", "lookup"]):
                    return [f"search {query}"]
                if any(w in query for w in ["notion", "launch notion", "open notion"]):
                    return [f"open open notion"]

            return [f"{label} {cleaned_query}"]

        except Exception:
            return [f"general {query}"]

    def classify(self, full_query: str) -> List[str]:
        full_query = full_query.lower()
        pattern = r'[,;:.!?]| and | then | but '
        split_phrases = re.split(pattern, full_query)

        tasks = []
        for phrase in split_phrases:
            phrase = phrase.strip(' "\'')
            if phrase and phrase not in ["after that", "also", "please", "then"]:
                tasks.extend(self.classify_single(phrase))
        return tasks

    def test_cli(self):
        print("[ Bro.ai Classifier Test Mode – type 'exit' to quit ]")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            result = self.classify(user_input)
            print("Bro.ai classified:", result)
            print("-" * 50)

if __name__ == "__main__":
    QueryClassifier().test_cli()
