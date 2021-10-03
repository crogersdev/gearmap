function importAll(r) {
    let images = {};
    r.keys().map(
        (item, index) => {
            images[item.replace('./', '')] = r(item); return null;
        }
    );
    
    return images;
}
const images = importAll(
    require.context('../assets/icons/', false, /\.(png|jpe?g|svg)$/)
);

export default images;