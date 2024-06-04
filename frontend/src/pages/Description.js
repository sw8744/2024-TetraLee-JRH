import './Description.css';
import { useSearchParams } from 'react-router-dom';
import Header from './Header';
import { useEffect, useState } from 'react';
import Footer from './Footer';

function Description() {
    const [searchParams] = useSearchParams();
    const id = searchParams.get('id');
    const clickedFood = searchParams.get('clickedFood');
    const [whereToEat, setWhereToEat] = useState('');
    const [info, setInfo] = useState('');
    const [amount, setAmount] = useState(0);

    const fetchId = async () => {
        fetch('http://127.0.0.1:5000/api/getinfo/' + id)
        .then(response => response.json())
        .then(data => {
            setWhereToEat(data.wheretoeat);
        });
    }

    const getClickedFood = async () => {
        fetch('http://127.0.0.1:5000/api/getfoodinfo/' + clickedFood)
        .then(response => response.json())
        .then(data => {
            setInfo(data[0]);
        });
    }



    useEffect(() => {
        fetchId();
        getClickedFood();
    }, []);

    return (
        <div>
            <Header whereToEat={whereToEat}/>
            <div className='description'>
                <div className='imgDiv'>
                    <img src={info.image} alt='food' className='foodImage'/>
                </div>
                <div className='titleDiv'>
                    <p className='foodName'>{info.name}</p>
                    <p className='price'>{info.price}원</p>
                </div>
                <div className='descDiv'>
                    <p className='title'>메뉴 설명</p>
                    <p className='description_txt'>{info.description}</p>
                    <p className='title'>주의 사항</p>
                    <p className='description_txt'>{info.caution}</p>
                </div>
            </div>
            <div className='buttonDiv'>
                <div className='amountDiv'>
                    <button className='minusButton'>-</button>
                    <p className='amount'>{amount}</p>
                    <button className='plusButton'>+</button>
                </div>
            </div>
            <Footer className='footer' />
        </div>
    );
};

export default Description;