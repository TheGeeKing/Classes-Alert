import json
from win10toast import ToastNotifier
from datetime import datetime, date
from time import sleep
import webbrowser

toaster = ToastNotifier()
now = datetime.now()

try:
  with open("config.json", "r") as config_jsonFile:
    config = json.load(config_jsonFile)
except:
  config = {}
  config["Info"] = {}
  config["Info"]["first_start"] = 1
  config["Info"]["start"] = 0
  config["Info"]["name"] = ""
  config["Info"]["next_course"] = ""
  config["Info"]["next_heure"] = ""
  config["Info"]["next_url"] = ""
  print(config)
  with open("config.json", "w") as config_jsonFile:
    json.dump(config ,config_jsonFile, indent=2, sort_keys=False)

def read_config():
  with open("config.json", "r") as config_jsonFile:
    config = json.load(config_jsonFile)

def write_config(config):
  with open("config.json", "w") as config_jsonFile:
    json.dump(config ,config_jsonFile, indent=2, sort_keys=False, ensure_ascii=False)

def first_start():
  global start
  read_config()
  if config["Info"]["first_start"] == 1:
    print("Salut, je vais t'aider à arriver en cours à l'heure! :)")
    print("Pour cela tu vas devoir me donner tes matières, tes heures de cours et si tu en as un, un lien!")
    print("Ensuite je t'enverrais une notification sur ton pc avant chaque cours! Si tu m'auras fourni un lien tu pourras cliquer sur la notification et ça l'ouvrira")
    while True:
      try:
        is_it_ok = str(input("ça te va? Y/N : "))
        is_it_ok = is_it_ok.upper()
        if len(is_it_ok) > 1:
          raise Exception
        elif len(is_it_ok) == 0:
          raise Exception
        else:
          if is_it_ok == "Y":
            print("Ok super c'est parti")
            read_config()
            config["Info"]["start"] = 1
            sleep(1)
            write_config(config)
            sleep(2)
            break
          elif is_it_ok == "N":
            print("Bon bah a+ alors")
            read_config()
            config["Info"]["start"] = 0
            write_config(config)
            sleep(1)
            break
          else:
            raise Exception      
      except:
        print("T'es un peu bête toi? Réponds moi par Y ou N")
        print(Exception)

def ask_subject():
  while True:
    try:
      subjects = ["Allemand", "English", "Art", "Espagnol", "French", "Histoire/Géographie/EMC", "HGGSP", "HLP", "Mandarin", "Mathématiques", "NSI", "OIB", "SES", "Sport"]
      answer_subject = int(input("""Choisissez le nombre correspondant à votre matière : \n1. Allemand\n2. Anglais\n3. Art\n4. Espagnol\n5. Français\n6. Histoire/Géographie/EMC\n7. HGGSP\n8. HLP\n9. Mandarin\n10. Mathématiques\n11. NSI\n12. OIB\n13. SES\n14 Sport\n"""))
      if answer_subject < 0:
        raise Exception
      elif answer_subject > 14:
        raise Exception
      else:
        global subject
        answer_subject -= 1
        subject = subjects[answer_subject]
      break
    except:
      print("Vous devez entrer un nombre!")

def ask_time(phrase_time):
  while True:
    try:
      times = ["08:30", "09:20", "10:10", "10:30", "11:20", "12:05", "12:25", "13:15", "14:05", "15:05", "15:55", "16:45", "17:35"]
      answer_time = int(input(f"""Choisissez le nombre correspondant à {phrase_time} : \n1. 08:30\n2. 09:20\n3. 10:10\n4. 10:30\n5. 11:20\n6. 12:05\n7. 12:25\n8. 13:15\n9. 14:05\n10. 15:05\n11. 15:55\n12. 16:45\n13. 17:35\n"""))
      if answer_time < 0:
        raise Exception
      elif answer_time > 13:
        raise Exception
      else:
        global time
        answer_time -= 1
        time = times[answer_time]
      break
    except:
      print("Vous devez entrer un nombre!")

def ask_link():
  while True:
    try:
      global link
      link = str(input("""Collez votre lien, sinon laissez vide : """))
      break
    except:
      print("Erreur : réponse non supportée")

def name_matiere(courses):
  list_cours = ["première", "seconde", "troisième", "quatrième", "cinquième", "sixième", "septième"]
  list_courses = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh"]
  courses_index = list_courses.index(f"{courses}")
  global course
  course = list_cours[courses_index]

def def_classes2(day):
  global subject, time, link
  with open("config.json", "r") as config_jsonFile:
    config = json.load(config_jsonFile)
  name_matiere(courses)
  print(f"Quelle est ta {course} matière {day}? : ")
  ask_subject()
  config["Week"][f"{day}"][f"{courses}"]["matiere"] = subject
  print("Quelle est l'heure de début? : ")
  ask_time("start time")
  config["Week"][f"{day}"][f"{courses}"]["heure_start"] = time
  print("Quelle est l'heure de fin? : ")
  ask_time("end time")
  config["Week"][f"{day}"][f"{courses}"]["heure_end"] = time
  ask_link()
  config["Week"][f"{day}"][f"{courses}"]["link"] = link
  write_config(config)

def number_courses(day):
  list_courses = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh"]
  while True:
    try:
      nombre_courses = int(input(f"Entrez le nombre de cours {day} : "))
      if nombre_courses < 0:
        raise Exception
      elif nombre_courses > 7:
        raise Exception
      else:
        with open("config.json", "r") as config_jsonFile:
          config = json.load(config_jsonFile)
        nombre_courses_index = nombre_courses
        nombre_courses_index -= 1
        x = 0
        course = list_courses[x]
        config["Week"][f"{day}"] = {}
        while x != nombre_courses_index+1:
          config["Week"][f"{day}"][f"{list_courses[x]}"] = {}
          x +=1
          with open("config.json", "w") as config_jsonFile:
            json.dump(config, config_jsonFile, indent=2, sort_keys=False)
        break
    except:
      print("Erreur : nombre non supportée")

def time_notif():
  while True:
    try:
      time_notif = int(input("""Choisissez le temps que avant que la notification disparaisse totalement (s):\n"""))
      if time_notif < 0:
        raise Exception
      elif time_notif > 600:
        raise Exception
      else:
        break
    except:
      print("Erreur : nombre non supportée")
  read_config()
  config["Info"]["time_notif"] = time_notif
  write_config(config)

def auto_open():
  while True:
    try:
      auto_open = int(input("""Choisissez si le lien s'ouvre automatiquement dans votre navigateur :\n1. Yes\n2. No\n"""))
      if auto_open == 1:
        break
      elif auto_open == 2:
        auto_open = 0
        break
      else:
        raise Exception
    except:
      print("Erreur : nombre non supportée")
  read_config()
  config["Info"]["auto_open"] = auto_open
  write_config(config)

def open_url(next_link):
  webbrowser.open(next_link, new=0, autoraise=True)

def check_auto_open(next_link):
  if config["Info"]["auto_open"] == 1:
    open_url(next_link)

def notif(next_link, next_course):
  if len(next_link) == 0:
    toaster.show_toast("Class Alert!", f"Prochain cours dans 5 minutes!\nVous aurez {next_course}", icon_path="MMA_DC.ico", duration=config["Info"]["time_notif"], threaded=True)
  else:
    toaster.show_toast("Class Alert!", f"Prochain cours dans 5 minutes!\nVous aurez {next_course}\nLe lien est : {next_link}", icon_path="MMA_DC.ico", duration=config["Info"]["time_notif"], threaded=True, callback_on_click=lambda: open_url(next_link))
    check_auto_open(next_link)

def print_course_notif(next_link, next_course):
  if len(next_link) == 0:
    print(f"Cours de {next_course} dans 5 minutes!")
  else:
    print(f"Cours de {next_course} dans moins de 5 minutes!!! Lien :",  next_link)

def check_time(today, course, next_course_start, next_link):
  while True:
    now_time = datetime.now().time()
    current_time_str = now.strftime("%H:%M")
    print("Prochain cours = ", next_course_start)
    next_course_start_time = datetime.strptime(next_course_start, "%H:%M").time()
    x = datetime.combine(date.today(), next_course_start_time) - datetime.combine(date.today(), now_time)
    y = str(x)
    if y.startswith("0:05:0"):
      print_course_notif(next_link, next_course)
      notif(next_link, next_course)
      break
    elif y < "0:":
      print_course_notif(next_link, next_course)
      notif(next_link, next_course)
      break
    elif y > "6:06":
      print(f"Il te reste {y}")
      sleep(60*60*6)
    elif y > "1:06":
      print(f"Il te reste {y}")
      sleep(60*60*1)
    elif y > "0:36":
      print(f"Il te reste {y}")
      sleep(60*30)
    elif y > "0:21":
      print(f"Il te reste {y}")
      sleep(60*15)
    else:
      print(f"Il te reste {y}")
      sleep(8)
      
read_config()
if config["Info"]["first_start"] == 1:
  first_start()

read_config()
if config["Info"]["start"] == 1:
  list_days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
  for day in list_days:
    number_courses(day)
  read_config()
  for day in config["Week"]:
    for courses in config["Week"][f"{day}"]:
      def_classes2(day)
  read_config()
  time_notif()
  auto_open()
  config["Info"]["first_start"] = 0
  write_config(config)

read_config()
if config["Info"]["first_start"] == 0:
  while True:
    current_day_datetime = now.strftime("%A")
    list_days_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    list_days_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    while True:
      try:
        day_index = list_days_en.index(f"{current_day_datetime}")
        break
      except:
        sleep(60)
    current_day = list_days_fr[day_index]
    read_config()
    auj = {}
    today = dict(config["Week"][f"{current_day}"])
    write_config(config)
    read_config()
    for course in today:
      write_config(config)
      read_config()
      course_matiere = course+"_matiere"
      auj["{0}".format(course_matiere)] = today[f"{course}"]["matiere"]
      current_time_str = now.strftime("%H:%M")
      next_course = today["{0}".format(course)]["matiere"]
      next_link = today["{0}".format(course)]["link"]
      next_course_start = today["{0}".format(course)]["heure_start"]
      if next_course_start<current_time_str:
        print(today[f"{course}"]["matiere"], "déjà passé")
      else: 
        print(today[f"{course}"]["matiere"], "pas encore passé")
        check_time(today, course, next_course_start, next_link)
        
      write_config(config)
    print("Plus de cours aujourd'hui à demain ;)")
    while now.strftime("%A") == current_day_datetime:
      sleep(60*60*8)