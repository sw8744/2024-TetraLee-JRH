import { useSearchParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import './Menu.css';

function Menu() {
    const [searchParams] = useSearchParams();
    const [menuKind, setMenuKind] = useState('');
    const [menu, setMenu] = useState('');
    const [clickedKind, setClickedKind] = useState('추천');
    const whereToEat = searchParams.get('whereToEat');
    
    const fetchKind = async () => {
        fetch('http://127.0.0.1:5000/api/kind')
        .then(response => response.json())
        .then(data => {
            let res = data.kind;
            res.splice(0, 0, "추천");
            setMenuKind(res);
        });
    };

    const fetchMenu = async () => {
        fetch('http://127.0.0.1:5000/api/menu')
        .then(response => response.json())
        .then(data => {
            setMenu(data);
        });
    }

    useEffect(() => {
        fetchKind();
        fetchMenu();
    }, []);


    return (
        <>
            <header className='header'>{whereToEat}</header>
            <div className='menuKindSelector'>
                {menuKind && menuKind.map((menu) => (
                <button className={
                    clickedKind === menu
                    ? 'menuKindButtonClicked'
                    : 'menuKindButton'
                } onClick={() => {setClickedKind(menu)}}>{menu}</button>
            ))}
            </div>
            <div className='menuSelector'>
                {menu && menu.map((menu) => (
                    <div className={
                        menu.selling === true
                        ? 'menu'
                        : 'menuSoldOut'
                    }>
                        <img src={menu.image} alt={menu.name} className='menuImg'/>
                        <div className='menuName'>{menu.name}</div>
                        {
                            menu.selling === true
                            ? <div className='menuPrice'>{menu.price}원</div>
                            : <div className='menuPrice'>품절</div>
                        }
                </div>
            ))}
            </div>
            <div className='orderSelector'>
                <button className='orderButton'>주문하기</button>
            </div>
        </>
    );
}

export default Menu;