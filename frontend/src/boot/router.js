let routerInstanceL = 0;

export default async ({ router }) => {
  // something to do
  routerInstanceL = router;
};

const RouterInstance = routerInstanceL;
export { RouterInstance };
