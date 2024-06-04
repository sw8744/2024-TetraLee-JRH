import './Header.css'
function Header(children) {
    const where = children.whereToEat;
    return (
        <header className='header'>{where}</header>
    );
}

export default Header;