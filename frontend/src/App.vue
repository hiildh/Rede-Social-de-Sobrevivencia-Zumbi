<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/register">Cadastro</router-link>
    </nav>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  nav {
    display: flex;
    justify-content: center;
    background-color: #2e8b57; /* Verde mais escuro */
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 0 0 10px 10px;
  }

  nav a {
    font-weight: bold;
    color: #fff;
    text-decoration: none;
    margin: 0 15px;
    padding: 10px 15px;
    border-radius: 5px;
    transition: background-color 0.3s ease;
  }

  nav a:hover {
    background-color: #3cb371; /* Verde mais claro */
  }

  nav a.router-link-exact-active {
    background-color: #228b22; /* Verde intermediário */
  }

  body {
    background-color: #e0f2f1; /* Fundo verde claro */
    margin: 0;
    padding: 0;
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
  }

  .register {
    max-width: 700px;
    margin: 40px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background: #fff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  fieldset {
    margin-bottom: 20px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }

  legend {
    padding: 0 10px;
    font-weight: bold;
    font-size: 1.2em;
    color: #2e8b57;
  }

  .form-group {
    margin-bottom: 15px;
  }

  .form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #2c3e50;
  }

  .form-group input,
  .form-group select {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 5px;
  }

  .inventory-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 20px;
  }

  .btn {
    display: inline-block;
    padding: 10px 20px;
    background-color: #2e8b57;
    color: #fff;
    text-decoration: none;
    border-radius: 5px;
    cursor: pointer;
    border: none;
    transition: background-color 0.3s ease;
  }

  .btn:hover {
    background-color: #3cb371;
  }
</style>
