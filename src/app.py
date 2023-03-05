from flask import Flask, render_template, request, url_for, redirect
import os 
import database as db 

template_dir= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir=os.path.join(template_dir, 'src','templates')

app=Flask(__name__, template_folder= template_dir)

#rutas de la app 

@app.route('/')
def home():
   cursor= db.database.cursor()
   cursor.execute("SELECT * FROM PEDIDO")
   myresult=cursor.fetchall()
   #convertir los datos a diccionario
   insertObject = []
   columnNames = [column[0] for column in cursor.description]
   for record in myresult:
       insertObject.append(dict(zip(columnNames, record)))
   cursor.close()    
   return render_template('index.html', data=insertObject)
#ruta para guardar
@app.route('/pedido', methods=['POST'])
def addpedido():
    nopedido=request.form['nopedido']
    operario=request.form['operario']
    referencia=request.form['referencia']
    tipo=request.form['tipo']
    inicio=request.form['inicio']
    bolsas=request.form['bolsas']
    fin=request.form['fin']

    if nopedido and operario and referencia and tipo and inicio:
        cursor = db.database.cursor()
        sql="insert into PEDIDO (nopedido,operario, referencia, tipo, inicio, bolsas, fin) values (%s,%s,%s,%s,%s,%s,%s)"
        data=(nopedido, operario, referencia, tipo,inicio, bolsas, fin)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:nopedido>')
def delete(nopedido):
        cursor = db.database.cursor()
        sql="delete from PEDIDO where nopedido=%s"
        data=(nopedido,)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('home'))

@app.route('/edit/<string:nopedido>', methods=['POST'])
def edit (nopedido):
    
    nopedido=request.form['nopedido']
    operario=request.form['operario']
    referencia=request.form['referencia']
    tipo=request.form['tipo']
    inicio=request.form['inicio']
    bolsas=request.form['bolsas']
    fin=request.form['fin']

    if nopedido and operario and referencia and tipo and inicio:
        cursor = db.database.cursor()
        sql="update PEDIDO set operario = %s, referencia = %s, tipo = %s, inicio =%s, bolsas = %s, fin = %s where nopedido = %s"
        data=( operario, referencia, tipo,inicio, bolsas, fin, nopedido)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

    

    


if __name__=='__main__':
    app.run(debug=True, port=4000)

