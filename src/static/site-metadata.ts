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

const data: ISiteMetadataResult = {
  siteTitle: "Jim's Running Journey",
  siteUrl: 'https://running.jimluo.com',
  logo: 'https://github.com/jimrory/running_page/blob/master/running.jpg?raw=true',
  description: "Jim's Running Journey",
  navLinks: [
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
