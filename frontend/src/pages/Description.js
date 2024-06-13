import './Description.css';
import { useSearchParams } from 'react-router-dom';
import Header from './Header';
import { useEffect, useState } from 'react';

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

    const getAmount = async () => {
        fetch('http://127.0.0.1:5000/api/getfoodamount/' + id + '/' + clickedFood)
        .then(response => response.json())
        .then(data => {
            setAmount(data.amount);
        });
    };

    useEffect(() => {
        fetchId();
        getClickedFood();
        getAmount();
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
                <button className='orderButton'>주문하기</button>
            </div>
            <footer className='footer2'>
                <button className='previousButton'>이전</button>
                <button className='nextButton'>다음</button>
            </footer>
        </div>
    );
};

export default Description;