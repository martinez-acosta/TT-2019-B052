export default function({ store, redirect }) {
  // If the user is not authenticated redirect to home page
  if (!store.getters['calls/loggedIn']) {
    return redirect('/')
  }
}
