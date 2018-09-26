from flask import Flask, request, render_template as f_render_template

from yugioh_wiki_scrape import wikia

app = Flask(__name__)
app.template_folder = "./public"

@app.route('/')
def root_page():
    context = {
        'rarity_data': [],
        'card_error': None,
    }
    if 'card_name' in request.args and request.args['card_name']:
        card = request.args['card_name'].replace(' ', '_')
        try:
            page = wikia.get_page(f'http://yugioh.wikia.com/wiki/{card}')
            table = wikia.get_english_tcg_table(page)
            data = wikia.get_table_data(table)
            print(data)
            data.sort(key=lambda row: wikia.TCG_RARITY.index(row[3].upper()), 
                reverse=True)
            table_data = [wikia.get_table_header(table), *data]
        except Exception as e:
            context['card_error'] = e
        else:
            context['rarity_data'] = table_data

    return render_template('index.html', **context)


def render_template(template: str, **context):
    context['_page'] = template
    return f_render_template('_main.html', **context)

    

if __name__ == '__main__':
    app.run(debug=True)