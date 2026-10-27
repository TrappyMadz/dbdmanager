<script setup lang="ts">
    import  { useRoute } from 'vue-router';
    const route = useRoute();
    console.log(route.params.id);
</script>

<template>
    <h1>Edit Patch Notes {{ route.params.id }}</h1>
</template>

<style scoped></style>
