<template>
  <div>Hola</div>
</template>

<script>
export default {
  middleware({ store, redirect }) {
    // If the user is not authenticated
    if (store.getters['calls/loggedIn']) {
      return redirect({ name: 'workspace-er' })
    } else return redirect('/')
  },
  layout: 'workspace'
}
</script>
