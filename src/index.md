---
toc: false
---

<div class="hero">
  <h1>CLC+ Delta</h1>
  <h2> European Big Data Hackathon 2025 Dashboard </h2>
</div>

<style>
.hero {
  /* Mise en page de base */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-family: var(--sans-serif);
  
  /* Marges et espacement */
  margin: 4rem 0;
  padding: 3rem 2rem;

  /* Arrière-plan doux */
  background: radial-gradient(circle, #f5f5f5 0%, #dddddd 100%);
  border-radius: 1rem;

  /* Légère ombre portée */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.07);

  /* Pour gérer l’éventuelle césure (si supporté) */
  text-wrap: balance;
}

.hero h1 {
  /* Organisation de l’espace autour du titre */
  margin: 1rem 0;
  padding: 1rem 0;

  /* Grande police pour le titre */
  font-size: clamp(3rem, 10vw, 6rem);
  font-weight: 900;
  line-height: 1.2;
  
  /* Effet de dégradé dans le texte */
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;

  /* Transition subtile au survol */
  transition: transform 0.3s ease;
}

.hero h1:hover {
  /* Léger agrandissement au hover */
  transform: scale(1.05);
}

.hero h2 {
  /* Mise en forme du sous-titre */
  margin: 0 auto;
  max-width: 40rem;
  font-size: 1.125rem;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
  
  /* Espace supplémentaire si souhaité */
  margin-top: 0.5rem;
}

@media (min-width: 640px) {
  .hero {
    margin: 6rem 0;
    padding: 4rem 3rem;
  }

  .hero h1 {
    font-size: clamp(4rem, 8vw, 7rem);
  }
}

</style>
