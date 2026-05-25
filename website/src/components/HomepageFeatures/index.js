import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

// Importa tus imágenes desde la carpeta static/img
import MooreTreeImage from '@site/static/img/image_0.png';
import BacktrackingImage from '@site/static/img/image_1.png';
import CageResultImage from '@site/static/img/image_2.png';

const FeatureList = [
  {
    title: 'La Cota de Moore (Árbol Base)',
    // Usa el componente imported Image para renderizar la foto
    Image: MooreTreeImage, 
    description: (
      <>
        El algoritmo toma como base el límite teórico inferior matemático. 
        Construye un árbol base que se expande por capas para intentar garantizar 
        la menor cantidad posible de vértices según el grado y el cuello.
      </>
    ),
  },
  {
    title: 'Búsqueda por Backtracking',
    Image: BacktrackingImage,
    description: (
      <>
        Implementa heurísticas avanzadas y técnicas de poda por isomorfismo. 
        El sistema detecta callejones sin salida de forma temprana, 
        evitando ciclos cortos y reduciendo drásticamente el tiempo de cómputo.
      </>
    ),
  },
  {
    title: 'Visualización y Generación',
    Image: CageResultImage,
    description: (
      <>
        Genera representaciones gráficas precisas de las jaulas resueltas. 
        A través de la integración con NetworkX y Matplotlib, renderiza 
        múltiples layouts matemáticos para analizar sus propiedades de simetría.
      </>
    ),
  },
];

function Feature({title, description, Image}) {
  return (
    <div className={clsx('col col--4')}>
      {/* Centramos la imagen y le damos un tamaño adecuado */}
      <div className="text--center">
        <img src={Image} className={styles.featureSvg} alt={title} style={{maxWidth: '200px', height: 'auto', marginTop: '2rem'}} />
      </div>
      <div className="text--center padding-horiz--md" style={{marginTop: '1rem'}}>
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}