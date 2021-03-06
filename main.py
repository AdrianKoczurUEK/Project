from flask import Flask, render_template, request, send_file, session
from functions import readJsFiles, saveAsJs, getJsonByItemId, sortBy, filterBy
from item import Item
from graph import generate_stars_plot,generate_recommend_plot

app = Flask(__name__)
app.config['SECRET_KEY'] = '8f42a73054b1749f8f58848be5e6502c'

@app.route('/author')
def author():
    return render_template('author.html', page='author')

@app.route('/graphs')
def item_graphs():
    item_id = request.args.get('id', None)
    item_data = getJsonByItemId(item_id)
    return render_template('graphs.html', plot_stars=generate_stars_plot(item_data),plot_recommend=generate_recommend_plot(item_data),item_id=item_id)

@app.route('/list')
def item_list():
    items_data = readJsFiles()
    return render_template('item_list.html', page='list', items_data=items_data)


@app.route('/download', methods=['POST'])
def downloadFile():
    path = request.form['downloadJson']
    return send_file(path, as_attachment=True)


@app.route('/')
def homePage():
    return render_template('index.html', page='home')


@app.route('/item/filter')
def itemFilter():
    opFilter = request.args.get('opFilter',None)
    item_id = session.get('my_item_id', None)
    item_data = getJsonByItemId(item_id)
    filtered_data = filterBy(item_data, opFilter)
    return render_template('item.html', user_data=filtered_data['item_reviews'], item_img=filtered_data['item_img'],
                           item_name=filtered_data['item_name'],item_id=filtered_data['item_id'])


@app.route('/item/sorted')
def itemSort():
    sort_by = request.args.get('sort', None)
    sort_rev = request.args.get('rev', None)
    item_id = session.get('my_item_id', None)
    item_data = getJsonByItemId(item_id)
    sorted_data = sortBy(item_data, sort_by, sort_rev)
    return render_template('item.html', user_data=sorted_data['item_reviews'], item_img=sorted_data['item_img'],
                           item_name=sorted_data['item_name'],item_id=sorted_data['item_id'])


@app.route('/extract')
def extract():
    return render_template('extract.html', page='extract')


@app.route('/item', methods=['POST'])
def item():
    try:
        item_id = request.form['item_id']
        item = Item(item_id)
        session['my_item_id'] = item_id
        saveAsJs(item.reviews, item_id, item)
        return render_template('item.html', user_data=item.reviews, item_img=item.img, item_name=item.item_name,item_id=item.item_id)
    except:
        return render_template('extract.html',page='extract',error=True)


if __name__ == '__main__':
    app.run(debug=True)
