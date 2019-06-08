import os 
from flask import Flask,render_template,send_from_directory,request,jsonify,redirect,url_for
import time
import paperclip

app = Flask(__name__,static_url_path = '')

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
#ALLOWED_EXTENSIONS = set(['txt','doc'])

#@app.route('/')
#def index():
    #return send_from_directory('templates','upload.html',as_attachment=True)

@app.route('/test')
def test():
    path = os.path.abspath('.')
    print(path)
    return send_from_directory(path,'trackerlist.txt',as_attachment=True)
    
@app.route('/')
def terminal():
    return render_template('terminal.html',
                                commands = [''])
@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/test/navigator/<targetDir>')
def navigator_test(targetDir):
    fileList = os.listdir("../"+targetDir)
    print(fileList) 
    return render_template('navigator.html',
                            files = fileList)

@app.route('/test/navigator/')
def navigator():
    fileList = os.listdir("../") 
    print(fileList)
    return render_template('navigator.html',
                            files = fileList)

@app.route('/api/upload',methods=['POST'],strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir,app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']
    fname = f.filename
    ext= fname.rsplit('.',1)[1]
    #unix_time = int(time.time())
    #new_filename = str(unix_time)+'.'+ext
    newDir = "../"+request.form['directory']
    if newDir:
        try:
            f.save(os.path.join(newDir,fname))
        except Exception as e:
            f.save(os.path.join(file_dir,fname))
            print(e)
    return render_template('upload.html')
    #return jsonify({"errno":0,"errmsg":"successfuly uploaded!"})
    
@app.route('/api/runscript',methods=['POST'],strict_slashes=False)
def api_runscript():
    scriptDir = "../"+request.form['scriptDir']
    os.system("python "+scriptDir)
    return jsonify({"errno":0,"errmsg":"successfuly running script!"})

@app.route('/api/terminal',methods=['POST'],strict_slashes=False)
def api_terminal():
    command = request.form['command']
    if command[0:2] == 'cd':#terminal command 'cd'
        os.chdir(command[3:])
        p = os.popen('dir')
    elif command[0:2] == 'dl':#download from server
        path = os.path.abspath('.')
        print(path)
        #return send_from_directory('../../'+path,command[3:],as_attachment=True)
        return send_from_directory(path,command[3:],as_attachment=True)
        p = os.popen('dir')
    elif command[0:2] == 'up': #open upload page
        return redirect('/upload')
    elif command[0:2] == 'pt':#print in server's console
        print(command[3:])
        p = command[3:]+'was sent to ras clipboard!' + '/n' +  os.popen('dir')
    elif command[0:2] == 'cp':#copy to server's clipboard
        paperclip.copy(command[3:])
        p = command[3:]+'was copied to ras clipboard!' + 'n' + os.popen('dir')
    elif command[0:2] == 'zp':
        path = os.path.abspath('.')
        fatherpath = os.path.abspath('..')
        folder = path[len(fatherpath)+1 : ]
        os.chdir('..')
        os.system("zip -r "+folder+".zip "+folder)
        print(path)
        print(fatherpath)
        os.chdir(folder)
        return send_from_directory(fatherpath,folder+'.zip',as_attachment=True)
        
    else:#terminal commmand
        p = os.popen(command) 
   
    echo = p.read()
    print(echo)
    return render_template('terminal.html',
                            commands = echo)

app.run(host = '0.0.0.0',port = 10200)
