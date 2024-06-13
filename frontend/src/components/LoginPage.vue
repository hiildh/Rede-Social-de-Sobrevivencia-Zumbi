<template>
    <div class="login">
        <h1>Bem-vindo à ZSSN</h1>
        <p>Por favor, insira seu nome para continuar:</p>
        <input v-model="survivorName" type="text" placeholder="Seu nome">
        <button @click="login">Entrar</button>
    </div>
</template>

<script>
    export default {
        name: 'LoginPage',
        data() {
            return {
                survivorName: ''
            };
        },
        methods: {
            async login() {
                try {
                    const response = await fetch(`http://localhost:8000/api/survivors/get-by-name/?name=${this.survivorName}`);
                    if (!response.ok) {
                        if (response.status === 401) {
                            throw new Error('Sobrevivente infectado');
                        }
                        throw new Error('Sobrevivente não encontrado');
                    }
                    const survivors = await response.json();
                    if (survivors.survivor.name == this.survivorName) {
                        const survivor = survivors.survivor;
                        this.$router.push({ name: 'Dashboard', params: { name: survivor.name } });
                    } else {
                        throw new Error('Sobrevivente não encontrado');
                    }
                } catch (error) {
                    alert('Erro: ' + error.message);
                }
            }
        }
    };
</script>

<style>
    .login {
        text-align: center;
        margin-top: 50px;
    }
    
    .login input {
        padding: 10px;
        font-size: 16px;
        margin-bottom: 20px;
    }
    
    .login button {
        padding: 10px 20px;
        background-color: #2e8b57;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    
    .login button:hover {
        background-color: #3cb371;
    }
</style>
