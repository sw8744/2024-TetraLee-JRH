import { useSearchParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import './Menu.css';
import Header from './Header';
import { useNavigate } from 'react-router-dom';


function Menu() {
    const [searchParams] = useSearchParams();
    const [menuKind, setMenuKind] = useState('');
    const [menu, setMenu] = useState('');
    const [clickedKind, setClickedKind] = useState('');
    const id = searchParams.get('id');
    const [whereToEat, setWhereToEat] = useState('');
    const [orderMenu, setOrderMenu] = useState('');
    const [clickedFood, setClickedFood] = useState('');
    const navigate = useNavigate();

    const fetchId = async () => {
        fetch('http://127.0.0.1:5000/api/getinfo/' + id)
        .then(response => response.json())
        .then(data => {
            setWhereToEat(data.wheretoeat);
        });
    };

    const fetchOrderMenu = async () => {
        fetch('http://127.0.0.1:5000/api/ordermenu/' + id)
        .then(response => response.json())
        .then(data => {
            setOrderMenu(data);
        });
    };
    
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

    const goNext = () => {
        navigate('/pay?id=' + id);
    }

    const goDescription = (clickedFood) => {
        clickedFood = clickedFood;
        navigate('/description?id=' + id + '&clickedFood=' + clickedFood);
    };

    useEffect(() => {
        fetchId();
        fetchKind();
        fetchMenu();
        fetchOrderMenu();
    }, []);

    return (
        <>
            <Header whereToEat={whereToEat}/>
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
                    }
                    id={menu.id} onClick={
                        menu.selling === true
                        ? () => goDescription(menu.id)
                        : null
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
                {orderMenu && orderMenu.map((menu) => (
                        <div className='orderMenu'
                        id={menu.id} onClick={() => goDescription(menu.id + 1)}>
                            <img src={menu.image} alt={menu.name} className='orderImg'/>
                            <div className='orderName'>{menu.name} × {menu.amount}</div>
                    </div>
                ))}
            </div>
            <footer className='footer1'>
                <button className='cancelButton'>주문 취소하기</button>
                <button className='payButton' onClick={goNext}>결제하기</button>
            </footer>
        </>
    );
}

export default Menu;