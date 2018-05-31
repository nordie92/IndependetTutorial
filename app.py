from flask import Flask, render_template, send_from_directory, request, make_response  
from pymongo import MongoClient
from bson.objectid import ObjectId
from random import randint
import os
import base64
import gridfs

client = MongoClient()
app = Flask(__name__ , template_folder='templates')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def newAllUsers():
    return{
        'users': [],
        'id' : 'allUsers'
    }

def newAllCourses():
    return{
        'courses': [],
        'id' : 'allCourses'
    }

def newEmptyUserCourse():
    return {
        'course':
        {
            'courseID': None
        }
    }

# Tutor ist auch nur ein User!
def newEmptyUser():
    return {
        'id': ObjectId(),
        'mail': None,
        'first_name': None,
        'last_name': None,
        'nickname': None,
        'passphrase': None,
        'isTutor': None,
        'courses': [],
        'ownCourses': []
    }


def newEmptyCourse():
    return {
        'id': ObjectId(),
        'name': None,
        'description': None,
        'courseBannerID': None,
        'categorys': {
            'documents': [],
            'quiz': []},
    }


def newDocument():
    return {
        'title': None,
        'id': ObjectId(),
        'styleTyp': None,
        'content': {
            'h1': [],
            'p': [],
            'courseImgID': None,
            'courseVideoID': None
        }
    }


def newQuiz():
    return {
        'name': None,
        'questions': []
    }


def newQuestion():
    return {
        'questionText': None,
        'answers': []
    }


def newAnswer():
    return {
        'answerText': None,
        'answerIsCorrect': None
    }


def fillDB():
    # DB-Connection
    db = client.myTestBase
    # Collection
    studCorp = db.studCorp
    # ------Define new Users/Tutors-------
    singleExampleUser = newEmptyUser()
    singleExampleUser['id'] = 1
    singleExampleUser['mail'] = 'm.maart@gmx.net'
    singleExampleUser['first_name'] = 'Moritz'
    singleExampleUser['last_name'] = 'Maart'
    singleExampleUser['nickname'] = 'nordie92'
    singleExampleUser['passphrase'] = 'Okay123'
    singleExampleUser['isTutor'] = False

    singleExampleUser2 = newEmptyUser()
    singleExampleUser2['id'] = 2
    singleExampleUser2['mail'] = 'me.mail@web.net'
    singleExampleUser2['first_name'] = 'Me'
    singleExampleUser2['last_name'] = 'Muster'
    singleExampleUser2['nickname'] = 'spaceboi'
    singleExampleUser2['passphrase'] = 'Jauuuu111'
    singleExampleUser2['isTutor'] = False

    singleExampleTutor = newEmptyUser()
    singleExampleTutor['id'] = 3
    singleExampleTutor['mail'] = 'a.b@c.de'
    singleExampleTutor['first_name'] = 'Le'
    singleExampleTutor['last_name'] = 'Ge'
    singleExampleTutor['nickname'] = 'lege1810'
    singleExampleTutor['passphrase'] = '12345'
    singleExampleTutor['isTutor'] = True

    newCourse = newEmptyUserCourse()
    newCourse['course']['courseID'] = '1'

    newCourse2 = newEmptyUserCourse()
    newCourse2['course']['courseID'] = '2'

    singleExampleUser['courses'].append(newCourse)
    singleExampleUser2['courses'].append(newCourse2)
    singleExampleTutor['ownCourses'].append(newCourse)

    allUsers = newAllUsers()

    allUsers['users'].append(singleExampleUser)
    allUsers['users'].append(singleExampleUser2)
    allUsers['users'].append(singleExampleTutor)

    studCorp.insert(allUsers)
    # ------------------Define new Tutorial-----------------------------------
    newTutorial = newEmptyCourse()
    #newTutorial['id'] = '1234567890qwertzuio2'
    newTutorial['name'] = 'Web-Systeme'
    newTutorial['description'] = 'Lernen sie Technologien zu vergleichen'

    newDoc = newDocument()
    newDoc['title'] = 'TestPage1'
    newDoc['styleTyp'] = 1
    newDoc['content']['link'] = 'rel="stylesheet" href="./css/design1.css"'
    newDoc['content']['h1'].append('Überschrift1 Bla Bla Bla')
    newDoc['content']['p'].append(
        'Das ist alles ein Paragraph bla bla bla ... bla bla bla')

    # #öffne Grid-Fs-Collection
    # db = client.myTestBase
    # fsCollection = gridfs.GridFS(db)

    # #für Kurs Banner
    # bannerID = ObjectId()
    # newTut['courseBannerID'] = bannerID
    # fsCollection.put(courseBanner, filename = courseBanner.filename, _id = bannerID)


    newDoc_1 = newDocument()
    newDoc_1['title'] = 'TestPageNummer 2'
    newDoc_1['styleTyp'] = 2

    newDoc_1['content']['link'] = 'rel="stylesheet" href="./css/design2.css"'
    newDoc_1['content']['h1'].append('WAS GEHT AB ÜBERSCHRIFT')
    newDoc_1['content']['p'].append(
        'Beispiel Paragraph')

    newExampleQuiz = newQuiz()
    newExampleQuiz['name'] = 'Quiz 1'

    newExampleQuestion = newQuestion()
    newExampleQuestion['questionText'] = 'Ist der Himmel für uns blau?'

    newExampleAnswer = newAnswer()
    newExampleAnswer['answerText'] = 'Ja'
    newExampleAnswer['answerIsCorrect'] = True

    newExampleAnswer2 = newAnswer()
    newExampleAnswer2['answerText'] = 'Nein'
    newExampleAnswer2['answerIsCorrect'] = False

    newExampleQuestion['answers'].append(newExampleAnswer)
    newExampleQuestion['answers'].append(newExampleAnswer2)

    newExampleQuiz['questions'].append(newExampleQuestion)

    newTutorial['categorys']['quiz'].append(newExampleQuiz)
    newTutorial['categorys']['documents'].append(newDoc)
    newTutorial['categorys']['documents'].append(newDoc_1)

    allCourses = newAllCourses()
    allCourses['id'] = 'allCourses'
    allCourses['courses'].append(newTutorial)

    #-----------------------------
    newTutorial2 = newEmptyCourse()
    #newTutorial2['id'] = '1234567890qwertzuio'
    newTutorial2['name'] = 'Mathe'
    newTutorial2['description'] = 'Integrale'

    newDoc2 = newDocument()
    newDoc2['title'] = 'TestPage1'
    newDoc2['styleTyp'] = 1
    newDoc2['content']['link'] = 'rel="stylesheet" href="./css/design1.css"'
    newDoc2['content']['h1'].append('Überschrift1 Bla Bla Bla')
    newDoc2['content']['p'].append(
        'Das ist alles ein Paragraph bla bla bla ... bla bla bla')

    newExampleQuiz2 = newQuiz()
    newExampleQuiz2['name'] = 'Quiz 1'

    newExampleQuestion2 = newQuestion()
    newExampleQuestion2['questionText'] = 'Ist der Himmel für uns blau?'

    newExampleAnswer2_1 = newAnswer()
    newExampleAnswer2_1['answerText'] = 'Ja'
    newExampleAnswer2_1['answerIsCorrect'] = True

    newExampleAnswer2_2 = newAnswer()
    newExampleAnswer2_2['answerText'] = 'Nein'
    newExampleAnswer2_2['answerIsCorrect'] = False

    newExampleQuestion2['answers'].append(newExampleAnswer2_1)
    newExampleQuestion2['answers'].append(newExampleAnswer2_2)

    newExampleQuiz2['questions'].append(newExampleQuestion2)

    newTutorial2['categorys']['quiz'].append(newExampleQuiz2)
    newTutorial2['categorys']['documents'].append(newDoc2)

    allCourses['courses'].append(newTutorial2)
    studCorp.insert(allCourses)


def getCollection():
    # DB-Connection
    db = client.myTestBase
    # Collection
    studCorp = db.studCorp
    return studCorp.find()

def deleteCollection():
    # DB-Connection
    db = client.myTestBase
    # Collection
    studCorp = db.studCorp
    gridFsFiles = db.fs.files
    gridFsChunks = db.fs.chunks
    db.drop_collection(gridFsFiles)
    db.drop_collection(gridFsChunks)
    db.drop_collection(studCorp)

def initDB():
    # DB-Connection
    db = client.myTestBase
    # Collection
    studCorp = db.studCorp
    allCourses = newAllCourses()
    allUsers = newAllUsers()

    studCorp.insert(allUsers)
    studCorp.insert(allCourses)

def getAllUsers():
    db = client.myTestBase
    studCorp = db.studCorp
    fullDB = studCorp.find()
    return fullDB[0]['users']

def getAllCoursesWrapperObject():
    db = client.myTestBase
    studCorp = db.studCorp
    fullDB = studCorp.find()
    return fullDB[1]

def getAllCourses():
    db = client.myTestBase
    studCorp = db.studCorp
    fullDB = studCorp.find()
    return fullDB[1]['courses']


def getCourse(courseID):
    allCourses = getAllCourses()
    foundcourse = {}
    for course in allCourses:
        if course['id'] == courseID:
            foundcourse = course
            break

    return foundcourse

def getCourseWithString(courseID):
    allCourses = getAllCourses()
    foundcourse = {}
    for course in allCourses:
        if str(course['id']) == courseID:
            foundcourse = course
            break

    return foundcourse

def getCourseIndex(courseID):
    allCourses = getAllCourses()
    courseIndex = 0
    for course in allCourses:
        if str(course['id']) != courseID:
            courseIndex += 1
        else:
            break

    if courseIndex >= len(allCourses):
        print("Fehler in getCourseIndex: Index out of range")

    return courseIndex


def getUser(cookieID):
    allUsers = getAllUsers()
    foundUser = {}
    for user in allUsers:
        if user['id'] == cookieID:
            foundUser = user
            break
    return foundUser


def getRand():
    return randint(0, 1000)


def getDocumentIndex(documentID, course):
    foundIndex = 0
    for documents in course['categorys']['documents']:
        if str(documents['id']) == documentID:
            break
        foundIndex += 1    
    if foundIndex >= len(course['categorys']['documents']):
        foundIndex = 0
        print("Fehler ")
        #raise Exception("Kein valides Dokument")
    return foundIndex


def renderTutorialTemplate(course, documentIndex,bannerImg, documentImg, videoID):
    # Unterscheidung des Template Styles
    templateToRender = None
    if int(course['categorys']['documents'][documentIndex]['styleTyp']) == 1:
        print("Template 1 ausgeführt")
        templateToRender = render_template('tutorialStyle1.html', user=getUser(
            1), course=course, documentID=course['categorys']['documents'][documentIndex]['id'], documentIndex=documentIndex, bannerImg = bannerImg,
            documentImg = documentImg, videoID = videoID)
    else:
        print("Template 2 ausgeführt")
        templateToRender = render_template('tutorialStyle2.html', user=getUser(
            1), course=course, documentID=course['categorys']['documents'][documentIndex]['id'], documentIndex=documentIndex,bannerImg = bannerImg,
            documentImg = documentImg)
    return templateToRender

#Liefert die ersten 6 Kurse
def getIndexTutorials(course):
    requiredCourses = {
        'Satz0' : [],
        'Satz1' : []
    }
    for i in range(0,6):
        if i < 3:
            if i < len(course):
                requiredCourses['Satz0'].append(course[i])
            else:
                requiredCourses['Satz0'].append(newEmptyCourse())
        else:
            if i < len(course):
                requiredCourses['Satz1'].append(course[i])
            else:
                requiredCourses['Satz1'].append(newEmptyCourse())
    return requiredCourses

def getCourseIfExists(courseID):
    course = None
    if courseID is not None:
        course = getCourseWithString(courseID)
    else:
        print("Tutorial nicht vorhanden")
    return course

# #funktion Später löschen, ist schon in getEncodedImageString
# def getBinaryJPGstring(courseID):
#     folder_name = '\\userData\\courseImages\\'
#     fullPath = APP_ROOT + format(folder_name) + format(courseID) + '.jpg'
#     print("Hier Full Path ", fullPath)

#     with open(fullPath, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#         decode=encoded_string.decode()
#     return 'data:image/jpg;base64,' + format(decode)

def isCourseOwner(userID, courseID):
    user = getUser(userID)
    userIsCourseOwner = False
    for ownCourses in user['ownCourses']:
        if ownCourses['course']['courseID'] == courseID:
            userIsCourseOwner = True
            break
    return userIsCourseOwner


def getEncodedImageString(imgid):
    #öffne Grid-Fs-Collection
    db = client.myTestBase
    fsCollection = gridfs.GridFS(db)
    encString = ''
    try:
        imageFile = fsCollection.get_last_version(_id=imgid)
        encoded_img_file = base64.b64encode(imageFile.read())
        decString = encoded_img_file.decode()
        filename = imageFile.filename
        ext = os.path.splitext(filename)[1]

        if (ext == ".jpg" or ext == ".JPG"):
            encString = 'data:image/jpg;base64,' + format(decString)
        elif (ext == ".png" or ext == ".PNG"):
            encString = 'data:image/png;base64,' + format(decString)
        elif (ext == ".jpeg" or ext == ".JPEG"):
            encString = 'data:image/jpeg;base64,' + format(decString)
        else:
            print("Fehler, Dateityp nicht zulässig: ", ext)
    except:
        print("Fehler in getEncodedImageString, Bild in DB nicht gefunden")

    return encString


def getEncodedVideoString(videoid):
    #öffne Grid-Fs-Collection
    db = client.myTestBase
    fsCollection = gridfs.GridFS(db)
    encString = ''
    try:
        videoFile = fsCollection.get_last_version(_id=videoid)
        encoded_video_file = base64.b64encode(videoFile.read())
        decString = encoded_video_file.decode()
        filename = videoFile.filename
        ext = os.path.splitext(filename)[1]

        if (ext == ".mp4" or ext == ".MP4"):
            encString = 'data:video/mp4;base64,' + format(decString)
        elif (ext == ".png" or ext == ".PNG"):
            encString = 'data:image/png;base64,' + format(decString)
        elif (ext == ".jpeg" or ext == ".JPEG"):
            encString = 'data:image/jpeg;base64,' + format(decString)
        else:
            print("Fehler, Dateityp nicht zulässig: ", ext)
    except:
        print("Fehler in getEncodedImageString, Bild in DB nicht gefunden")

    return encString




def updateDataBase(whatToUpdate, document):
    db = client.myTestBase
    studCorp = db.studCorp
    try:
        docSelector = {"id": whatToUpdate}
        studCorp.update_one(docSelector, {"$set": document})
    except Exception:
        print("Fehler in UpdateDataBase, Dokument zum updaten nicht gefunden.")
    

@app.route('/uploadTestIndex')
def tempTest():
    return render_template('upload.html')


#Wenn Tutorial schon existiert
#@app.route('/editTutorial', methods=['POST'])
#def editTutorial():
# userID = request.args.get('cookieID')
# courseID = request.args.get('courseID')
# if isCourseOwner(userID, courseID)
# courseIndex = getCourseIndex(courseID)
# allCourses = getAllCoursesWrapperObject()
#bearbeite KursInformationen
# allCourses['courses'][courseIndex]['courseImgID'] = imgID

# @app.route('/testUploadCourseImg', methods=['GET'])
# def testUploadCourseImg():


def getCourseBanner(courseID):
    #suche Kurs
    foundCourse = getCourse(courseID)
    #suche Bild ID
    emptyCourse = {}
    encString = ''
    if foundCourse != emptyCourse:
        
        bannerID = foundCourse['courseBannerID']
        if bannerID == None:
            print("Kurs besitzt kein Banner")
            return ''
        #suche Grid DB ab, und gebe verschlüsselten String mit Dateityp zurück
        encString = getEncodedImageString(bannerID)
    return encString

def getCourseIMG(courseID,documentID):
    #suche Kurs
    foundCourse = getCourseWithString(courseID)
    #suche Bild ID im jeweiligen Dokument
    imgID = foundCourse['categorys']['documents'][getDocumentIndex(documentID, foundCourse)]['content']['courseImgID']
    #suche Grid DB ab, und gebe verschlüsselten String mit Dateityp zurück
    encString = getEncodedImageString(imgID)
    return encString

def getCourseVideo(courseID,documentID):
    #suche Kurs
    foundCourse = getCourseWithString(courseID)
    #suche Bild ID im jeweiligen Dokument
    videoID = foundCourse['categorys']['documents'][getDocumentIndex(documentID, foundCourse)]['content']['courseVideoID']
    #suche Grid DB ab, und gebe verschlüsselten String mit Dateityp zurück
    encString = getEncodedVideoString(videoID)
    return encString

@app.route('/uploadTutorial', methods=['POST'])
def uploadTutorial():
    #userID = request.args.get('cookieID')
    #if userIsTutor(userID)
    #...

    courseBanner = request.files.getlist('courseBanner')
    courseName =  request.form.get('courseName')
    courseDescription = request.form.get('courseDescription')
    
    #für jede Seite im Tutorial
    pagesTitle = request.form.getlist('pageTitle')
    pagesStyle = request.form.getlist('pageStyle')
    pagesVideo = request.files.getlist('videoFile')
    pagesText =  request.form.getlist('docText')
    pagesText2 = request.form.getlist('docText2')
    pagesImg =   request.files.getlist('courseImg')
    

    newTut = newEmptyCourse()
    newTut['name'] = courseName
    newTut['description'] = courseDescription

    #öffne Grid-Fs-Collection
    db = client.myTestBase
    fsCollection = gridfs.GridFS(db)

    #für Kurs-banner
    bannerID = ObjectId()
    newTut['courseBannerID'] = bannerID
    fsCollection.put(courseBanner[0], filename = courseBanner[0].filename, _id = bannerID)
    #für alle Kurse
    countPages =  request.form.get('countPages')
    for x in range(0, int(countPages)):

        #für Kurs Img/video
        imgID = ObjectId()
        videoID = ObjectId()

        #Neues Dokument
        newDoc = newDocument()
        newDoc['title'] = pagesTitle[x]
        newDoc['content']['courseImgID'] = imgID
        newDoc['content']['courseVideoID'] = videoID
        newDoc['styleTyp'] = pagesStyle[x]
        newDoc['content']['p'].append(pagesText[x])
        newDoc['content']['p'].append(pagesText2[x])
        fsCollection.put(pagesImg[x], filename = pagesImg[x].filename, _id = imgID)
        rawVideo = pagesVideo[x].read()
        fsCollection.put(rawVideo, filename = pagesVideo[x].filename, _id = videoID)
        newTut['categorys']['documents'].append(newDoc)
    

    #hänge neuen Kurs an alle Kurse ran
    allCourses = getAllCoursesWrapperObject()
    allCourses['courses'].append(newTut)
    #update alle Kurse in DB
    updateDataBase('allCourses', allCourses)

    #testweise
    return render_template('tutorialSuccessfulyUploaded.html')

#Um auf Seite 1 zu kommen, wenn Tutorial geöffnet wird.
@app.route('/Tutorial', methods=['GET'])
def getTutorialWithoutDocumentID():
    courseID = request.args.get('courseID')
    course = getCourseIfExists(courseID)

    #documentIndex immer 0, wenn Tutorial ohne Dokument geöffnet wird
    documentIndex = 0
    docID = course['categorys']['documents'][documentIndex]['id']
    #hole Files ab
    bannerImg = getCourseBanner(courseID)
    documentImg = getCourseIMG(courseID, docID)
    videoID = course['categorys']['documents'][documentIndex]['content']['courseVideoID']
    #documentVideo = getCourseVideo(courseID, docID)
    return renderTutorialTemplate(course, documentIndex,bannerImg,documentImg,videoID)

#Um auf die anderen Seiten des Tutorials zu kommen
@app.route('/Tutorial/', methods=['GET'])
def getTutorialWithDocumentID():
    # cookieID =  #readCookie()
    courseID = request.args.get('courseID')
    course = getCourseIfExists(courseID)
   
    documentID = request.args.get('documentID')
    if documentID is not None:
        documentIndex = getDocumentIndex(documentID, course)
    else:
        documentIndex = 0
    
    bannerImg = getCourseBanner(courseID)
    documentImg = getCourseIMG(courseID, documentID)
    videoID = course['categorys']['documents'][documentIndex]['content']['courseVideoID']
    #documentVideo = getCourseVideo(courseID, documentID)
    return renderTutorialTemplate(course, documentIndex,bannerImg,documentImg,videoID)


@app.route('/index', methods=['GET'])
def getIndex():
    courses = getAllCourses()
    requiredCourses = getIndexTutorials(courses)
    for course in requiredCourses['Satz0']:
        if course['id'] != None:
            course['courseImg']  = getCourseBanner(course['id'])

    for course in requiredCourses['Satz1']:
        if course['id'] != None:
            course['courseImg']  = getCourseBanner(course['id'])

    return render_template('index.html', courses = requiredCourses)


#--------Get BootStrap-Content-Routen-------
@app.route('/assets/bootstrap/css/<filename>')
def send_bootStrapCss(filename):
    return send_from_directory("templates/assets/bootstrap/css", filename)

@app.route('/assets/bootstrap/js/<filename>')
def send_bootStrapJs(filename):
    return send_from_directory("templates/assets/bootstrap/js", filename)

@app.route('/assets/css/<filename>')
def send_css(filename):
    return send_from_directory("templates/assets/css", filename)

@app.route('/assets/fonts/<filename>')
def send_fonts(filename):
    return send_from_directory("templates/assets/fonts", filename)

@app.route('/assets/img/<filename>')
def send_image(filename):
    return send_from_directory("templates/assets/img", filename)

@app.route('/assets/js/<filename>')
def send_js(filename):
    return send_from_directory("templates/assets/js", filename)
#------------------------------------------------
@app.route('/video/<videoid>')
def getVideo(videoid):
    #öffne Grid-Fs-Collection
    db = client.myTestBase
    fsCollection = gridfs.GridFS(db)
    videoFile = fsCollection.get_last_version(_id = ObjectId(videoid)) 
    filename = videoFile.filename
    print("DateiName: ", filename)
    
    response = make_response(videoFile.read())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    return response




# startpunkt des py-programms
if __name__ == "__main__":
   deleteCollection()
   initDB()
   #fillDB() 

   app.run(debug=True, host='0.0.0.0')

