import './Receipt.css';
import { useState } from 'react';
import Header from './Header';
import { useSearchParams } from 'react-router-dom';

function Receipt() {
    const [number, setNumber] = useState(0);
    const [searchParams] = useSearchParams();
    const whereToEat = searchParams.get('whereToEat');
    return (
        <>
            <Header whereToEat={whereToEat}/>
            <div>
                <p className='finishPay'>결제가 완료되었습니다.<br/></p>
                <p className='receipt'>영수증을</p>
                <p className='receipt'>출력하시겠습니까?</p>
            </div>
            <div className='buttonDiv'>
                <button className='yesButton'>예</button>
                <button className='noButton'>아니오</button>
            </div>
            <div className='numberDiv'>
                <p className='number'>주문 번호 {number}번</p>
            </div>
        </>
    );
}

export default Receipt;