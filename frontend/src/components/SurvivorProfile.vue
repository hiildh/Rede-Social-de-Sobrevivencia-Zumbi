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
                survivor: null
            };
        },
        created() {
            this.fetchSurvivorData();
        },
        methods: {
            async fetchSurvivorData() {
                const name = this.$route.params.name;
                try {
                    const response = await fetch(`http://localhost:8000/api/survivors/?name=${name}`);
                    if (response.ok) {
                    const survivors = await response.json();
                    if (survivors.length > 0) {
                        this.survivor = survivors[0];
                    } else {
                        throw new Error('Sobrevivente não encontrado');
                    }
                    } else {
                    throw new Error('Erro ao buscar dados do sobrevivente');
                    }
                } catch (error) {
                    console.error('Erro ao buscar dados do sobrevivente:', error);
                }
            }
        }
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
