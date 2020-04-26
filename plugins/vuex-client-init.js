export default async (context) => {
  await context.store.dispatch('calls/nuxtClientInit', context)
}
