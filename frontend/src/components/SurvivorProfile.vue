<template>
    <div class="profile">
        <h1>Perfil do Sobrevivente</h1>
        <div v-if="survivor">
            <p><strong>Nome:</strong> {{ survivor.name }}</p>
            <p><strong>Idade:</strong> {{ survivor.age }}</p>
            <p><strong>Gênero:</strong> {{ survivor.gender }}</p>
            <p><strong>Última Localização:</strong> {{ survivor.last_location }}</p>
            <!-- Adicione mais informações conforme necessário -->
        </div>
        <div v-else>
            <p>Carregando...</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'SurvivorProfile',
        data() {
        return {
            survivor: null,
        };
        },
        created() {
        this.fetchSurvivorData();
        },
        methods: {
        async fetchSurvivorData() {
            const uniqueCode = this.$route.params.uniqueCode;
            try {
            const response = await fetch(`http://localhost:8000/api/survivors/${uniqueCode}/`);
            const data = await response.json();
            this.survivor = data;
            } catch (error) {
            console.error('Erro ao buscar dados do sobrevivente:', error);
            }
        },
        },
    };
</script>

<style>
    /* Estilos para o perfil */
    .profile {
        text-align: center;
        padding: 50px;
    }

    .profile h1 {
        font-size: 2rem;
        margin-bottom: 20px;
    }

    .profile p {
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
</style>
