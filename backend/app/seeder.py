from .db.database import SessionLocal, engine
from .db.models import Base, InformationSource, Category, RSSChannel, Role, User, CrossRoleUser

roles_iniciales = [
    {"name": "LECTOR"},
    {"name": "GESTOR"},
    {"name": "ADMINISTRADOR"},
]

categorias_iptc = [
    {"code": "01000000", "name": "Artes, cultura, entretenimiento y medios"},
    {"code": "03000000", "name": "Catástrofes y accidentes"},
    {"code": "13000000", "name": "Ciencia y tecnología"},
    {"code": "16000000", "name": "Conflicto, guerra y paz"},
    {"code": "15000000", "name": "Deporte"},
    {"code": "04000000", "name": "Economía, negocios y finanzas"},
    {"code": "05000000", "name": "Educación"},
    {"code": "10000000", "name": "Estilo de vida y tiempo libre"},
    {"code": "08000000", "name": "Interés humano, animales, insólito"},
    {"code": "09000000", "name": "Mano de obra"},
    {"code": "06000000", "name": "Medio ambiente"},
    {"code": "17000000", "name": "Meteorología"},
    {"code": "02000000", "name": "Policía y justicia"},
    {"code": "11000000", "name": "Política"},
    {"code": "12000000", "name": "Religión y culto"},
    {"code": "07000000", "name": "Salud"},
    {"code": "14000000", "name": "Sociedad"},
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
    {"name": "ONU Noticias", "url": "https://news.un.org/es"},
]

canales_rss = [
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

    {"source_name": "ESDiario", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.esdiario.com/rss/viajes.xml"},
    {"source_name": "ESDiario", "category_name": "Salud", "url": "https://www.esdiario.com/rss/salud.xml"},
    {"source_name": "ESDiario", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.esdiario.com/rss/chismografo/recetas.xml"},
    {"source_name": "ESDiario", "category_name": "Ciencia y tecnología", "url": "https://www.esdiario.com/rss/motor.xml"},
    {"source_name": "ESDiario", "category_name": "Artes, cultura, entretenimiento y medios", "url": "https://www.esdiario.com/rss/chismografo/medios.xml"},
    {"source_name": "ESDiario", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.esdiario.com/rss/chismografo/estilo.xml"},
    {"source_name": "ESDiario", "category_name": "Política", "url": "https://www.esdiario.com/rss/nacional.xml"},
    {"source_name": "ESDiario", "category_name": "Sociedad", "url": "https://www.esdiario.com/rss/opinion.xml"},
    {"source_name": "ESDiario", "category_name": "Economía, negocios y finanzas", "url": "https://www.esdiario.com/rss/economia.xml"},
    {"source_name": "ESDiario", "category_name": "Estilo de vida y tiempo libre", "url": "https://www.esdiario.com/rss/chismografo/tendencias.xml"},

    {"source_name": "Antena 3", "category_name": "Sociedad", "url": "https://www.antena3.com/noticias/rss/4013050.xml"},

    {"source_name": "Ministerio de Consumo", "category_name": "Sociedad", "url": "https://www.dsca.gob.es/es/rss-noticias.xml"},
    {"source_name": "Ministerio de Consumo", "category_name": "Educación", "url": "https://www.dsca.gob.es/es/rss-publicaciones.xml"},

    {"source_name": "Ministerio de Economía", "category_name": "Mano de obra", "url": "https://portal.mineco.gob.es/_layouts/15/rss.aspx?c=em&l=%7B2862B654%2DE4C2%2D4C40%2DAD48%2D9A94120B1B37%7D&v=%7B7515627D%2DF7C9%2D46E9%2DBFFF%2D7A289F859316%7D&s=/es-es/ministerio/empleo"},
    {"source_name": "Ministerio de Economía", "category_name": "Política", "url": "https://portal.mineco.gob.es/_layouts/15/rss.aspx?c=le&l=%7B3604CB7A%2DFA50%2D460E%2DA563%2DFC19E37689D8%7D&v=%7B25A4E419%2DEEE9%2D4D11%2D9691%2D04652E0F4E05%7D&s=/"},
    {"source_name": "Ministerio de Economía", "category_name": "Economía, negocios y finanzas", "url": "https://portal.mineco.gob.es/_layouts/15/rss.aspx?c=pu&l=%7B8833FFD2-4D84-4171-A9B3-68812F17079E%7D&v=%7BA394FD57-F1DE-4AA9-8B14-21CAEE55DDC5%7D&s=/es-es/ministerio/publicaciones/electronicas"},
    {"source_name": "Ministerio de Economía", "category_name": "Política", "url": "https://portal.mineco.gob.es/_layouts/15/rss.aspx?c=np&l=%7BDE1040A8-90D1-4F24-9455-423894813206%7D&v=%7B5B3B491D-EFBE-4286-9DA1-A6C04483F78D%7D&s=/es-es/comunicación"},
    {"source_name": "Ministerio de Economía", "category_name": "Economía, negocios y finanzas", "url": "https://portal.mineco.gob.es/_layouts/15/rss.aspx?c=gm&l=%7B880B017C%2D7E33%2D43DA%2DB86A%2DB86671E51E6F%7D&v=%7B7EEF8CD3%2DC48C%2D4DE8%2D9E38%2D8023C31DD7AD%7D&s=/es-es/economiayempresa/unidadmercado/gum/buscador"},

    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=17"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=16"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=15"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=32"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/Paginas/rss.aspx?tipo=23"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=22"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=20"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=2"},
    {"source_name": "La Moncloa", "category_name": "Política", "url": "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=1"},

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

    {"source_name": "Aciprensa", "category_name": "Religión y culto", "url": "https://www.aciprensa.com/rss/noticias.xml"},
    {"source_name": "Aciprensa", "category_name": "Religión y culto", "url": "https://www.aciprensa.com/rss/news/espana"},
    {"source_name": "Aciprensa", "category_name": "Religión y culto", "url": "https://www.aciprensa.com/rss/news/vaticano"},
    {"source_name": "Aciprensa", "category_name": "Religión y culto", "url": "https://www.aciprensa.com/rss/evangelio"},
    {"source_name": "Aciprensa", "category_name": "Religión y culto", "url": "https://www.aciprensa.com/rss/saints"},
    {"source_name": "Aciprensa", "category_name": "Religión y culto", "url": "https://www.aciprensa.com/rss/news/vida-y-familia"},

    {"source_name": "Europa Press", "category_name": "Catástrofes y accidentes", "url": "https://www.europapress.es/rss/rss.aspx?ch=00073"},
    {"source_name": "Europa Press", "category_name": "Policía y justicia", "url": "https://www.europapress.es/rss/rss.aspx?ch=00066"},

    {"source_name": "ONU Noticias", "category_name": "Conflicto, guerra y paz", "url": "https://news.un.org/feed/subscribe/es/news/topic/peace-and-security/feed/rss.xml"},
]


def _apply_migrations(engine):
    from sqlalchemy import inspect, text
    insp = inspect(engine)
    if "category" in insp.get_table_names():
        cols = [c["name"] for c in insp.get_columns("category")]
        if "code" not in cols:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE category ADD COLUMN code VARCHAR(8)"))
                conn.commit()

        # Remove categories seeded with IPTC-code integer PKs (id >= 1000000).
        # The new seeder uses auto-increment IDs so that the API can create
        # IPTC-code-ID categories (id = int(iptc_code)) without conflicts.
        with engine.connect() as conn:
            rows = conn.execute(
                text("SELECT id FROM category WHERE id >= 1000000")
            ).fetchall()
            if rows:
                for (row_id,) in rows:
                    conn.execute(
                        text("DELETE FROM rss_channel WHERE category_id = :id"),
                        {"id": row_id},
                    )
                    conn.execute(
                        text("DELETE FROM category WHERE id = :id"),
                        {"id": row_id},
                    )
                conn.commit()


def seed_db():
    _apply_migrations(engine)

    db = SessionLocal()
    try:
        # Roles
        role_map = {}
        for r in roles_iniciales:
            role = db.query(Role).filter(Role.name == r["name"]).first()
            if not role:
                role = Role(name=r["name"])
                db.add(role)
                db.commit()
                db.refresh(role)
            role_map[r["name"]] = role.id

        # Usuario administrador inicial
        admin_email = "admin@newsradar.com"
        if not db.query(User).filter(User.email == admin_email).first():
            admin_role_id = role_map.get("ADMINISTRADOR")
            admin = User(
                email=admin_email,
                password="admin123",
                first_name="Admin",
                last_name="NewsRadar",
                organization="NewsRadar",
                is_verified=True,
            )
            db.add(admin)
            db.flush()
            if admin_role_id:
                db.add(CrossRoleUser(user_id=admin.id, role_id=admin_role_id))
            db.commit()

        # Categorías IPTC — use auto-increment IDs so the API can assign
        # IPTC-code-based IDs (int(code)) without conflicting with seeded rows.
        # source stores the 8-digit IPTC code so SMOKE-005 can extract it via
        # _extract_iptc_code without needing a 'code' field in the API response.
        cat_map = {}
        for c in categorias_iptc:
            cat = db.query(Category).filter(Category.name == c["name"]).first()
            if not cat:
                cat = Category(name=c["name"], source=c["code"], code=c["code"])
                db.add(cat)
                db.commit()
                db.refresh(cat)
            else:
                changed = False
                if cat.code != c["code"]:
                    cat.code = c["code"]
                    changed = True
                if cat.source != c["code"]:
                    cat.source = c["code"]
                    changed = True
                if changed:
                    db.commit()
                    db.refresh(cat)
            cat_map[c["name"]] = cat.id

        # Fuentes de información
        source_map = {}
        for m in medios:
            source = db.query(InformationSource).filter(InformationSource.name == m["name"]).first()
            if not source:
                source = InformationSource(name=m["name"], url=m["url"])
                db.add(source)
                db.commit()
                db.refresh(source)
            source_map[m["name"]] = source.id

        # Canales RSS
        for canal in canales_rss:
            source_id = source_map.get(canal["source_name"])
            cat_id = cat_map.get(canal["category_name"])
            if source_id and cat_id:
                if not db.query(RSSChannel).filter(RSSChannel.url == canal["url"]).first():
                    db.add(RSSChannel(
                        information_source_id=source_id,
                        category_id=cat_id,
                        url=canal["url"],
                    ))
        db.commit()
        print("[seeder] Base de datos inicializada correctamente.")

    except Exception as e:
        print(f"[seeder] Error: {e}")
        db.rollback()
    finally:
        db.close()
