<script setup lang="ts"></script>

<template>
  <nav>
    <RouterLink to="/">Home</RouterLink>
    <RouterLink to="/patchnotes">Patch Notes</RouterLink>
    <RouterLink to="/admin/patchnotes">Patch Notes Admin</RouterLink>
    <RouterLink to="/admin/patchnotes/edit/1">Edit Patch Notes</RouterLink>
    <RouterLink to="/admin/patchnotes/new">New Patch Notes</RouterLink>
    <RouterLink to="/404">404</RouterLink>
  </nav>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
  nav {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
  }
</style>
