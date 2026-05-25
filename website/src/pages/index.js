import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        {/* Aquí puedes agregar un logo si tienes uno en static/img/logo.png */}
        {/* <img src="img/logo.png" width="150" style={{marginBottom: '20px'}} /> */}
        
        <Heading as="h1" className="hero__title" style={{color: '#ffffff'}}>
          {siteConfig.title} 
        </Heading>
        <p className="hero__subtitle" style={{color: '#cbd5e0', fontSize: '1.5rem'}}>
          {siteConfig.tagline}
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/kage"> {/* 👈 Asegúrate que coincida con tu nombre de archivo */}
            Ver Documentación 
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Inicio | ${siteConfig.title}`}
      description="Documentación oficial del Proyecto Kage para la generación de (k,g)-jaulas matemáticas.">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}