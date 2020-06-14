import mechanize
from bs4 import BeautifulSoup as bs
import http.cookiejar as cookielib
import sys

#senha = sys.argv[2]

def busca_mercadolivre(txt) :
        
    strBusca = txt.replace(' ','-')


    cookies = cookielib.CookieJar()  # cria um repositório de cookies
    browser = mechanize.Browser()    # inicia um browser
    browser.set_cookiejar(cookies)   # aponta para o seu repositório de cookies
    browser.set_handle_robots(False)

    # carrega a pagina
    browser.open('https://lista.mercadolivre.com.br/'+strBusca)

    # carrega a pagina do perfil logado

    pagina = browser.response().read()  # pega o HTML 

    #print(pagina)
    # Beautiful Soup aqui
    soup = bs(pagina,'html.parser')
    codigo = soup.find_all(True,{"class":"item__info-link"})

    if len(codigo) == 0 :
        codigo = soup.find_all(True,{"class":"item__info"})
     
    print(codigo)

    strResultado = ""
    listaResultado = []
    
    for dados in codigo :
        print(dados.find(class_='main-title').text)
        nomeProduto = dados.find(class_='main-title').text
        precoProduto = ""

        try:
            #print(dados.find(class_='item__price').find(class_='price__symbol').text)
            precoSimboloProduto = dados.find(class_='item__price').find(class_='price__symbol').text
            precoValorProduto = dados.find(class_='item__price').find(class_='price__fraction').text
            try:
                precoCentavoProduto = ","+dados.find(class_='item__price').find(class_='price__decimals').text
            except AttributeError :
                precoCentavoProduto = ""
            
            
            precoProduto = precoSimboloProduto +" "+precoValorProduto + precoCentavoProduto
            print(precoProduto)
        except AttributeError :
             print(dados.find(class_='pdp_options__text').text)
             precoProduto = dados.find(class_='pdp_options__text').text
        
        
        #nomeProduto = dados.text
        linkProduto = ""

        try:
            linkProduto = dados.get("href")

            if linkProduto is None :
                linkProduto = dados.find(class_='item__info-title').get("href")    
        except AttributeError :
            print(dados)
            #linkProduto = dados.find(class_='item__info-title').get("href")
        
        print(linkProduto)

        try:
            listaResultado.append( nomeProduto +"\n"+precoProduto+"\n"+linkProduto+"\n")
        except TypeError :
            #print(dados.find(class_='item__info-title').get("href"))
            pass
    return listaResultado


if __name__ == "__main__" :
    #print(sys.argv)
    if len(sys.argv) < 2 :
        print("Falta argumentos:")
        print("Uso: "+sys.argv[0]+" <busca+produto>")
        exit(1)

    txt = ""

    for argumento in sys.argv[1:] :
        txt += argumento+" "

    busca_mercadolivre(txt[0:-1])


