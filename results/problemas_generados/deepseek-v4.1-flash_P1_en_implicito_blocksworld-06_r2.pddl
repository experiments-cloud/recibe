(define (problem blocksworld-six)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (clear d)
    (clear f)
    (handempty)
    (on a c)
    (on d a)
    (on e b)
    (on f e)
    (ontable b)
    (ontable c)
  )
  (:goal (and
    (on c b)
    (on b a)
    (on a e)
    (on e f)
    (on f d)
  ))
)
