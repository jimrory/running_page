interface ISiteMetadataResult {
  siteTitle: string;
  siteUrl: string;
  description: string;
  logo: string;
  navLinks: {
    name: string;
    url: string;
  }[];
}

const getBasePath = () => {
  const baseUrl = import.meta.env.BASE_URL;
  return baseUrl === '/' ? '' : baseUrl;
};

const data: ISiteMetadataResult = {
  siteTitle: "jim's running journey",
  siteUrl: 'https://running.jimluo.com',
  logo: 'https://running.jimluo.com/images/logo.png',
  description: "jim's running journey",
  navLinks: [
    {
      name: 'Summary',
      url: `${getBasePath()}/summary`,
    },
    {
      name: 'ins',
      url: 'https://www.instagram.com/jimrory',
    },
    {
      name: 'about',
      url: 'https://jimluo.com',
    },
  ],
};

export default data;
