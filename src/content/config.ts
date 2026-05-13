import { defineCollection, z } from 'astro:content';

const projectsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    repo: z.string(),
    category: z.string(),
    description: z.string(),
    excerpt: z.string(),
    thumbnail: z.string().optional(),
    githubUrl: z.string(),
    stars: z.number().default(0),
    language: z.string().optional(),
    featured: z.boolean().default(false),
    priority: z.number().default(99),
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = {
  projects: projectsCollection,
};
