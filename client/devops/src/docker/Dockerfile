FROM node:8 as react-build
WORKDIR /gearmap_ui
COPY . .
RUN yarn
RUN yarn build

FROM nginx:alpine
COPY --from=react-build /gearmap_ui/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
