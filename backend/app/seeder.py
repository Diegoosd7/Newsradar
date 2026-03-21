from db.database import SessionLocal, engine
from db.models import Base, InformationSource, Category, RSSChannel

# 1. Definir los datos iniciales
categorias_iptc = [
    {"name": "Artes, cultura, entretenimiento y medios", "source": "IPTC"},
    {"name": "Catástrofes y accidentes", "source": "IPTC"},
    {"name": "Ciencia y tecnología", "source": "IPTC"},
    {"name": "Conflicto, guerra y paz", "source": "IPTC"},
    {"name": "Deporte", "source": "IPTC"},
    {"name": "Economía, negocios y finanzas", "source": "IPTC"},
    {"name": "Educación", "source": "IPTC"},
    {"name": "Estilo de vida y tiempo libre", "source": "IPTC"},
    {"name": "Interés humano, animales, insólito", "source": "IPTC"},
    {"name": "Mano de obra", "source": "IPTC"},
    {"name": "Medio ambiente", "source": "IPTC"},
    {"name": "Meteorología", "source": "IPTC"},
    {"name": "Policía y justicia", "source": "IPTC"},
    {"name": "Política", "source": "IPTC"},
    {"name": "Religión y culto", "source": "IPTC"},
    {"name": "Salud", "source": "IPTC"},
    {"name": "Sociedad", "source": "IPTC"}
]

medios = [
    {"name": "RTVE", "url": "https://www.rtve.es"},
    {"name": "El País", "url": "https://elpais.com"},
    {"name": "ABC", "url": "https://www.abc.es"},
    {"name": "El Confidencial", "url": "https://www.elconfidencial.com"},
    {"name": "Marca", "url": "https://www.marca.com"},
    {"name": "ESDiario", "url": "https://www.esdiario.com"},
    {"name": "Antena 3", "url": "https://www.antena3.com"},
    {"name": "Ministerio de Consumo", "url": "https://www.dsca.gob.es"},
    {"name": "Ministerio de Economía", "url": "https://portal.mineco.gob.es"},
    {"name": "La Moncloa", "url": "https://www.lamoncloa.gob.es"},
    {"name": "La Vanguardia", "url": "https://www.lavanguardia.com"},
    {"name": "Aciprensa", "url": "https://www.aciprensa.com"},
    {"name": "Europa Press", "url": "https://www.europapress.es"},
    {"name": "ONU Noticias", "url": "https://news.un.org/es"}
]

canales_rss = [
    # --- RTVE ---
    {"source_name": "RTVE", "category_name": "Sociedad", "url": "https://api2.rtve.es/rss/temas_noticias.xml"},
    {"source_name": "RTVE", "category_name": "Deporte", "url": "https://api2.rtve.es/rss/temas_deportes.xml"},
    {"source_name": "RTVE", "category_name": "Ciencia y tecnología", "url": "https://api2.rtve.es/rss/temas_ciencia-tecnologia.xml"},
    {"source_name": "RTVE", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://api2.rtve.es/rss/temas_cultura.xml"},
    {"source_name": "RTVE", "category_name": "Meteorología", "url": "https://api2.rtve.es/rss/temas_tiempo.xml"},
    {"source_name": "RTVE", "category_name": "Política", "url": "https://api2.rtve.es/rss/temas_espana.xml"},
    {"source_name": "RTVE", "category_name": "Política", "url": "https://api2.rtve.es/rss/temas_mundo.xml"},
    {"source_name": "RTVE", "category_name": "Sociedad", "url": "https://api2.rtve.es/rss/temas_comunidad-madrid.xml"},
    {"source_name": "RTVE", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://api2.rtve.es/rss/temas_oscar.xml"},
    {"source_name": "RTVE", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://api2.rtve.es/rss/temas_premios-goya.xml"},

    # --- EL PAÍS ---
    {"source_name": "El País", "category_name": "Política", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/internacional/portada"},
    {"source_name": "El País", "category_name": "Política", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada"},
    {"source_name": "El País", "category_name": "Ciencia y tecnología", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/tecnologia/portada"},
    {"source_name": "El País", "category_name": "Economía, negocios y finanzas", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/economia/portada"},
    {"source_name": "El País", "category_name": "Estilo de vida y tiempo libre", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/estilo/portada"},
    {"source_name": "El País", "category_name": "Deporte", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/deportes/portada"},
    {"source_name": "El País", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/television/portada"},
    {"source_name": "El País", "category_name": "Estilo de vida y tiempo libre", "url": "https://feeds.elpais.com/mrss-s/list/ep/site/elpais.com/section/smoda"},
    {"source_name": "El País", "category_name": "Medio ambiente", "url": "https://feeds.elpais.com/mrss-s/list/ep/site/elpais.com/section/clima-y-medio-ambiente"},
    {"source_name": "El País", "category_name": "Educación", "url": "https://feeds.elpais.com/mrss-s/list/ep/site/elpais.com/section/educacion"},
    {"source_name": "El País", "category_name": "Estilo de vida y tiempo libre", "url": "https://feeds.elpais.com/mrss-s/list/ep/site/elpais.com/section/gastronomia"},

    # --- ABC ---
    {"source_name": "ABC", "category_name": "Salud", "url": "https://www.abc.es/rss/2.0/bienestar/psicologia-sexo/"},
    {"source_name": "ABC", "category_name": "Salud", "url": "https://www.abc.es/rss/2.0/bienestar/alimentacion/"},
    {"source_name": "ABC", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.abc.es/rss/2.0/estilo/decoracion/"},
    {"source_name": "ABC", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.abc.es/rss/2.0/estilo/belleza/"},
    {"source_name": "ABC", "category_name": "Interés humano, animales, insólito", "url": "https://www.abc.es/rss/2.0/gente/"},
    {"source_name": "ABC", "category_name": "Deporte", "url": "https://www.abc.es/rss/2.0/deportes/"},
    {"source_name": "ABC", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://www.abc.es/rss/2.0/cultura/toros/"},
    {"source_name": "ABC", "category_name": "Sociedad", "url": "https://www.abc.es/rss/2.0/opinion/"},
    {"source_name": "ABC", "category_name": "Sociedad", "url": "https://www.abc.es/rss/2.0/ultima-hora/"},
    {"source_name": "ABC", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.abc.es/rss/2.0/summum/"},

    # --- EL CONFIDENCIAL ---
    {"source_name": "El Confidencial", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://rss.elconfidencial.com/tags/otros/musica-5272/"},
    {"source_name": "El Confidencial", "category_name": "Deporte", "url": "https://rss.elconfidencial.com/deportes/"},
    {"source_name": "El Confidencial", "category_name": "Ciencia y tecnología", "url": "https://rss.elconfidencial.com/tecnologia/"},
    {"source_name": "El Confidencial", "category_name": "Sociedad", "url": "https://rss.elconfidencial.com/sociedad/"},
    {"source_name": "El Confidencial", "category_name": "Política", "url": "https://rss.elconfidencial.com/mundo/"},
    {"source_name": "El Confidencial", "category_name": "Salud", "url": "https://rss.elconfidencial.com/tags/otros/salud-6110/"},
    {"source_name": "El Confidencial", "category_name": "Estilo de vida y tiempo libre", "url": "https://rss.vanitatis.elconfidencial.com/estilo/"},
    {"source_name": "El Confidencial", "category_name": "Interés humano, animales, insólito", "url": "https://rss.vanitatis.elconfidencial.com/casas-reales/"},
    {"source_name": "El Confidencial", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://rss.elconfidencial.com/tags/otros/libros-5344/"},
    {"source_name": "El Confidencial", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://rss.elconfidencial.com/tags/otros/cine-7354/"},
    {"source_name": "El Confidencial", "category_name": "Mano de obra", "url": "https://rss.elconfidencial.com/tags/economia/trabajo-5284/"},

    # --- MARCA ---
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/futbol/primera-division.xml"},
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/futbol/segunda-division.xml"},
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/futbol/futbol-sala.xml"},
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/futbol/champions-league.xml"},
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/futbol/europa-league.xml"},
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/futbol/premier-league.xml"},
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/baloncesto/acb.xml"},
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/baloncesto/nba.xml"},
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/motor/formula1.xml"},
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/motor/motogp.xml"},
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/atletismo.xml"},
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/ciclismo.xml"},
    {"source_name": "Marca", "category_name": "Deporte", "url": "https://objetos.estaticos-marca.com/rss/tenis.xml"},

    # --- ESDIARIO ---
    {"source_name": "ESDiario", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.esdiario.com/rss/viajes.xml"},
    {"source_name": "ESDiario", "category_name": "Salud", "url": "https://www.esdiario.com/rss/salud.xml"},
    {"source_name": "ESDiario", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.esdiario.com/rss/chismografo/recetas.xml"},
    {"source_name": "ESDiario", "category_name": "Ciencia y tecnología", "url": "https://www.esdiario.com/rss/motor.xml"}, # Motor puede ser tecnología o deporte
    {"source_name": "ESDiario", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://www.esdiario.com/rss/chismografo/medios.xml"},
    {"source_name": "ESDiario", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.esdiario.com/rss/chismografo/estilo.xml"},
    {"source_name": "ESDiario", "category_name": "Política", "url": "https://www.esdiario.com/rss/nacional.xml"},
    {"source_name": "ESDiario", "category_name": "Sociedad", "url": "https://www.esdiario.com/rss/opinion.xml"},
    {"source_name": "ESDiario", "category_name": "Economía, negocios y finanzas", "url": "https://www.esdiario.com/rss/economia.xml"},
    {"source_name": "ESDiario", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.esdiario.com/rss/chismografo/tendencias.xml"},

    # --- ANTENA 3 ---
    {"source_name": "Antena 3", "category_name": "Sociedad", "url": "https://www.antena3.com/noticias/rss/4013050.xml"},

    # --- MINISTERIO DE CONSUMO ---
    {"source_name": "Ministerio de Consumo", "category_name": "Sociedad", "url": "https://www.dsca.gob.es/es/rss-noticias.xml"},
    {"source_name": "Ministerio de Consumo", "category_name": "Educación", "url": "https://www.dsca.gob.es/es/rss-publicaciones.xml"},

    # --- MINISTERIO DE ECONOMÍA ---
    {"source_name": "Ministerio de Economía", "category_name": "Mano de obra", "url": "https://portal.mineco.gob.es/_layouts/15/rss.aspx?c=em&l=%7B2862B654%2DE4C2%2D4C40%2DAD48%2D9A94120B1B37%7D&v=%7B7515627D%2DF7C9%2D46E9%2DBFFF%2D7A289F859316%7D&s=/es-es/ministerio/empleo"},
    {"source_name": "Ministerio de Economía", "category_name": "Política", "url": "https://portal.mineco.gob.es/_layouts/15/rss.aspx?c=le&l=%7B3604CB7A%2DFA50%2D460E%2DA563%2DFC19E37689D8%7D&v=%7B25A4E419%2DEEE9%2D4D11%2D9691%2D04652E0F4E05%7D&s=/"},
    {"source_name": "Ministerio de Economía", "category_name": "Economía, negocios y finanzas", "url": "https://portal.mineco.gob.es/_layouts/15/rss.aspx?c=pu&l=%7B8833FFD2-4D84-4171-A9B3-68812F17079E%7D&v=%7BA394FD57-F1DE-4AA9-8B14-21CAEE55DDC5%7D&s=/es-es/ministerio/publicaciones/electronicas"},
    {"source_name": "Ministerio de Economía", "category_name": "Política", "url": "https://portal.mineco.gob.es/_layouts/15/rss.aspx?c=np&l=%7BDE1040A8-90D1-4F24-9455-423894813206%7D&v=%7B5B3B491D-EFBE-4286-9DA1-A6C04483F78D%7D&s=/es-es/comunicación"},
    {"source_name": "Ministerio de Economía", "category_name": "Economía, negocios y finanzas", "url": "https://portal.mineco.gob.es/_layouts/15/rss.aspx?c=gm&l=%7B880B017C%2D7E33%2D43DA%2DB86A%2DB86671E51E6F%7D&v=%7B7EEF8CD3%2DC48C%2D4DE8%2D9E38%2D8023C31DD7AD%7D&s=/es-es/economiayempresa/unidadmercado/gum/buscador"},

    # --- LA MONCLOA ---
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=17"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=16"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=15"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=32"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/Paginas/rss.aspx?tipo=23"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=22"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=20"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=2"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=1"},

    # --- LA VANGUARDIA ---
    {"source_name": "La Vanguardia", "category_name": "Catástrofes y accidentes", "url": "https://www.lavanguardia.com/rss/sucesos.xml"},
    {"source_name": "La Vanguardia", "category_name": "Política", "url": "https://www.lavanguardia.com/rss/politica.xml"},
    {"source_name": "La Vanguardia", "category_name": "Sociedad", "url": "https://www.lavanguardia.com/rss/local/madrid.xml"},
    {"source_name": "La Vanguardia", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.lavanguardia.com/rss/vida.xml"},
    {"source_name": "La Vanguardia", "category_name": "Deporte", "url": "https://www.lavanguardia.com/rss/deportes.xml"},
    {"source_name": "La Vanguardia", "category_name": "Economía, negocios y finanzas", "url": "https://www.lavanguardia.com/rss/economia.xml"},
    {"source_name": "La Vanguardia", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://www.lavanguardia.com/rss/cultura.xml"},
    {"source_name": "La Vanguardia", "category_name": "Interés humano, animales, insólito", "url": "https://www.lavanguardia.com/rss/gente.xml"},
    {"source_name": "La Vanguardia", "category_name": "Sociedad", "url": "https://www.lavanguardia.com/rss/participacion.xml"},
    {"source_name": "La Vanguardia", "category_name": "Medio ambiente", "url": "https://www.lavanguardia.com/rss/natural.xml"},
    {"source_name": "La Vanguardia", "category_name": "Salud", "url": "https://www.lavanguardia.com/rss/vida/salud.xml"},
    {"source_name": "La Vanguardia", "category_name": "Ciencia y tecnología", "url": "https://www.lavanguardia.com/rss/tecnologia.xml"},
    {"source_name": "La Vanguardia", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://www.lavanguardia.com/rss/television.xml"},
    {"source_name": "La Vanguardia", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://www.lavanguardia.com/rss/series.xml"},
    {"source_name": "La Vanguardia", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.lavanguardia.com/rss/ocio/viajes.xml"},
    {"source_name": "La Vanguardia", "category_name": "Ciencia y tecnología", "url": "https://www.lavanguardia.com/rss/motor.xml"},
    {"source_name": "La Vanguardia", "category_name": "Interés humano, animales, insólito", "url": "https://www.lavanguardia.com/rss/mascotas.xml"},
    {"source_name": "La Vanguardia", "category_name": "Sociedad", "url": "https://www.lavanguardia.com/rss/mamas-y-papas.xml"},
    {"source_name": "La Vanguardia", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.lavanguardia.com/rss/comer.xml"},
    {"source_name": "La Vanguardia", "category_name": "Política", "url": "https://www.lavanguardia.com/rss/internacional.xml"},
    {"source_name": "La Vanguardia", "category_name": "Ciencia y tecnología", "url": "https://www.lavanguardia.com/rss/ciencia.xml"},

    # --- ACIPRENSA ---
    {"source_name": "Aciprensa", "category_name": "Religión y culto", "url": "https://www.aciprensa.com/rss/noticias.xml"},
    {"source_name": "Aciprensa", "category_name": "Religión y culto", "url": "https://www.aciprensa.com/rss/news/espana"},
    {"source_name": "Aciprensa", "category_name": "Religión y culto", "url": "https://www.aciprensa.com/rss/news/vaticano"},
    {"source_name": "Aciprensa", "category_name": "Religión y culto", "url": "https://www.aciprensa.com/rss/evangelio"},
    {"source_name": "Aciprensa", "category_name": "Religión y culto", "url": "https://www.aciprensa.com/rss/saints"},
    {"source_name": "Aciprensa", "category_name": "Religión y culto", "url": "https://www.aciprensa.com/rss/news/vida-y-familia"},

    # --- EUROPA PRESS ---
    {"source_name": "Europa Press", "category_name": "Catástrofes y accidentes", "url": "https://www.europapress.es/rss/rss.aspx?ch=00073"},
    {"source_name": "Europa Press", "category_name": "Policía y justicia", "url": "https://www.europapress.es/rss/rss.aspx?ch=00066"}, 
    
    # --- ONU NOTICIAS ---
    {"source_name": "ONU Noticias", "category_name": "Conflicto, guerra y paz", "url": "https://news.un.org/feed/subscribe/es/news/topic/peace-and-security/feed/rss.xml"}
]

def seed_db():
    Base.metadata.create_all(bind=engine) # Crea las tablas si no existen
    db = SessionLocal()

    try:
        # 1. Insertar Categorías
        cat_map = {}
        for c in categorias_iptc:
            cat = db.query(Category).filter_by(name=c["name"]).first()
            if not cat:
                cat = Category(name=c["name"], source=c["source"])
                db.add(cat)
                db.commit()
                db.refresh(cat)
            cat_map[c["name"]] = cat.id

        # 2. Insertar Medios
        source_map = {}
        for m in medios:
            source = db.query(InformationSource).filter_by(name=m["name"]).first()
            if not source:
                source = InformationSource(name=m["name"], url=m["url"])
                db.add(source)
                db.commit()
                db.refresh(source)
            source_map[m["name"]] = source.id

        # 3. Insertar Canales RSS
        for canal in canales_rss:
            source_id = source_map.get(canal["source_name"])
            cat_id = cat_map.get(canal["category_name"])
            
            if source_id and cat_id:
                rss = db.query(RSSChannel).filter_by(url=canal["url"]).first()
                if not rss:
                    new_rss = RSSChannel(
                        information_source_id=source_id,
                        category_id=cat_id,
                        url=canal["url"]
                    )
                    db.add(new_rss)
        
        db.commit()
        print("¡Base de datos inicializada con éxito!")
        
    except Exception as e:
        print(f"Error cargando datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()