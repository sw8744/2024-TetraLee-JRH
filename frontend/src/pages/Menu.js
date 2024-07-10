import { useSearchParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import './Menu.css';
import Header from './Header';
import { useNavigate } from 'react-router-dom';
import getSpeech from '../util/GetSpeech';


function Menu() {
    const [searchParams] = useSearchParams();
    const [menuKind, setMenuKind] = useState('');
    const [menu, setMenu] = useState('');
    const [menuFinal, setMenuFinal] = useState(menu);
    const [recommendMenu, setRecommendMenu] = useState('');
    const [clickedKind, setClickedKind] = useState('');
    const id = searchParams.get('id');
    const [whereToEat, setWhereToEat] = useState('');
    const [orderMenu, setOrderMenu] = useState('');
    const [age, setAge] = useState('');
    const navigate = useNavigate();

    const fetchId = async () => {
        await fetch('http://127.0.0.1:5000/api/getinfo/' + id)
        .then(response => response.json())
        .then(data => {
            setWhereToEat(data.wheretoeat);
            setAge(data.age);
        });
    };

    const fetchAge = async () => {
        await fetch('http://127.0.0.1:5000/api/getinfo/' + id)
        .then(response => response.json())
        .then(data => {
            sleep(100);
            setAge(data.age);
        });
    };

    const fetchOrderMenu = async () => {
        await fetch('http://127.0.0.1:5000/api/ordermenu/' + id)
        .then(response => response.json())
        .then(data => {
            setOrderMenu(data);
        });
    };
    
    const fetchKind = async () => {
        await fetch('http://127.0.0.1:5000/api/kind')
        .then(response => response.json())
        .then(data => {
            let res = data.kind;
            res.splice(0, 0, "추천");
            setMenuKind(res);
        });
    };

    const fetchMenu = async () => {
        await fetch('http://127.0.0.1:5000/api/menu')
        .then(response => response.json())
        .then(data => {
            setMenu(data);
        });
    }

    const fetchRecommend = async () => {
        await fetch('http://127.0.0.1:5000/api/menu/' + age)
        .then(response => response.json())
        .then(data => {
            setRecommendMenu(data);
        });
    };

    const goPrevious = () => {
        navigate('/');
    }

    const goNext = () => {
        navigate('/howtopay?id=' + id);
    }

    const goDescription = (clickedFood) => {
        navigate('/description?id=' + id + '&clickedFood=' + clickedFood);
    };

    const setShowMenu = (clickedKind) => {
        if (menu && clickedKind === '') {
            setMenuFinal(menu);
        } 
        else if(recommendMenu && clickedKind === '추천') {
            setMenuFinal(recommendMenu);
        }
        else if(menu){
            let res = menu.filter((menu) => menu.kind === clickedKind);
            setMenuFinal(res);
        }
        else {
            setMenuFinal('');
        }
    }

    const clickKind = (kind) => {
        if(clickedKind === kind) {
            setClickedKind('');
            setShowMenu('');
        }
        else if(kind === '추천') {
            setClickedKind(kind);
            setShowMenu(kind);
        }
        else {
            setClickedKind(kind);
            setShowMenu(kind);
        }
    }

    function sleep(ms) {
        const wakeUpTime = Date.now() + ms;
        while (Date.now() < wakeUpTime) {}
    }

    useEffect(() => {
        fetchId();
        fetchKind();
        fetchMenu();
        fetchOrderMenu();
        getSpeech('메뉴를 선택해주세요.');
    }, []);

    useEffect(() => {
        fetchAge();
    }, [whereToEat]);

    useEffect(() => {
        if(age !== '') {
            fetchRecommend();
        }
    }, [whereToEat, age]);
    
    useEffect(() => {
        setShowMenu(clickedKind);
    }, [whereToEat, age, recommendMenu]);

    return (
        <>
            <Header whereToEat={whereToEat}/>
            <div className='menuKindSelector'>
                {menuKind && menuKind.map((menu) => (
                <button className={
                    clickedKind === menu
                    ? 'menuKindButtonClicked'
                    : 'menuKindButton'
                } onClick={() => clickKind(menu)}>{menu}</button>
            ))}
            </div>
            <div className='menuSelector'>
                {menuFinal && menuFinal.map((menu) => (
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
                <button className='cancelButton' onClick={goPrevious}>주문 취소하기</button>
                <button className='payButton' onClick={goNext}>결제하기</button>
            </footer>
        </>
    );
}

export default Menu;